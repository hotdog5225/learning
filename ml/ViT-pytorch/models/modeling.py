# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import logging
import math

from os.path import join as pjoin

import torch
import torch.nn as nn
import numpy as np

from torch.nn import CrossEntropyLoss, Dropout, Softmax, Linear, Conv2d, LayerNorm
from torch.nn.modules.utils import _pair
from scipy import ndimage

import models.configs as configs

from .modeling_resnet import ResNetV2


logger = logging.getLogger(__name__)


ATTENTION_Q = "MultiHeadDotProductAttention_1/query"
ATTENTION_K = "MultiHeadDotProductAttention_1/key"
ATTENTION_V = "MultiHeadDotProductAttention_1/value"
ATTENTION_OUT = "MultiHeadDotProductAttention_1/out"
FC_0 = "MlpBlock_3/Dense_0"
FC_1 = "MlpBlock_3/Dense_1"
ATTENTION_NORM = "LayerNorm_0"
MLP_NORM = "LayerNorm_2"


def np2th(weights, conv=False):
    """Possibly convert HWIO to OIHW."""
    if conv:
        weights = weights.transpose([3, 2, 0, 1])
    return torch.from_numpy(weights)


def swish(x):
    return x * torch.sigmoid(x)


ACT2FN = {"gelu": torch.nn.functional.gelu, "relu": torch.nn.functional.relu, "swish": swish}


class Attention(nn.Module):
    def __init__(self, config, vis):
        super(Attention, self).__init__()
        self.vis = vis
        # wzw, 多头注意力机制, num_attention_heads:12 (head个数)
        self.num_attention_heads = config.transformer["num_heads"]
        # wzw, hidden_size(768, 特征的维度), attent_head_size:64(768/12,每个head贡献多少维度)
        self.attention_head_size = int(config.hidden_size / self.num_attention_heads)
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        # wzw, q,k,v三个向量, 是由三个全连接层生成的(三个权重矩阵QKV), 注意输入和输出维度一致, 才能多层叠加
        self.query = Linear(config.hidden_size, self.all_head_size)
        self.key = Linear(config.hidden_size, self.all_head_size)
        self.value = Linear(config.hidden_size, self.all_head_size)

        # MLP全连接层
        self.out = Linear(config.hidden_size, config.hidden_size)
        self.attn_dropout = Dropout(config.transformer["attention_dropout_rate"])
        self.proj_dropout = Dropout(config.transformer["attention_dropout_rate"])

        # softmax, 对q*k的结果进行权重分配
        self.softmax = Softmax(dim=-1)

    def transpose_for_scores(self, x): # wzw, x(512, 197, 768)
        # wzw, x.size()[:-1]: 这表示取张量形状的前 n-1 个维度
        # wzw, + (self.num_attention_heads, self.attention_head_size)
        #   这表示在前 n-1 个维度后，添加两个新的维度。
        #   self.num_attention_heads 是注意力头的数量，
        #   self.attention_head_size 是每个注意力头的大小。
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size) # new_x_shape(512, 197, 12, 64)
        # wzw, x.view(*new_x_shape) 是一种常用的方法，用于重新调整张量 x 的形状而不改变其数据
        x = x.view(*new_x_shape) # x(512, 197, 12, 64)
        return x.permute(0, 2, 1, 3) # wzw, permute 用于重新排列张量的维度

    def forward(self, hidden_states): # hidden_states:(512, 197, 768), 得到的序列
        # wzw, 获取各个序列的qkv. QKV矩阵是所有序列共享的.
        # wzw, 获取query(mixed_query_layer(512,197,768))
            # wzw, hidden_states(512, 197, 768) 构建好的序列特征
            # wzw, query(全链接层Linear(in_feature=768, our_feature=768, bias=True))
        mixed_query_layer = self.query(hidden_states)
        # wzw, 获取key
        mixed_key_layer = self.key(hidden_states)
        # wzw, 获取value
        mixed_value_layer = self.value(hidden_states)

        # wzw, 为了后面q*k做内积, 进行一下矩阵变换
        query_layer = self.transpose_for_scores(mixed_query_layer) # wzw, query_layer(512, 12, 197, 64)
        key_layer = self.transpose_for_scores(mixed_key_layer) # wzw, 维度同上
        value_layer = self.transpose_for_scores(mixed_value_layer) # wzw, 维度同上

        # wzw, 算每个head的q*k(权重 or score)
        # attention_scores(512, 12, 197, 197)
        #   512batch_size, 12个head, 197*197是因为序列(len 197)的每个元素都要和序列所有元素计算一个权重.
        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2)) # wzw,  key_layer.transpose(-1, -2) (512, 12, 64, 197)
        # wzw, 正则项, 算内积(特征维度越大,内积越大)
        attention_scores = attention_scores / math.sqrt(self.attention_head_size)
        # wzw, 内积是值, softmax转换成权重
        attention_probs = self.softmax(attention_scores) # wzw (512, 12, 197, 197)
        weights = attention_probs if self.vis else None
        attention_probs = self.attn_dropout(attention_probs)

        # 获取value (q*k*v)
        context_layer = torch.matmul(attention_probs, value_layer) # context_layer(512, 12, 197, 64)
        # 将多头拼接起来(12head, 每个head64dim, 拼起来12*64=768), 还原成(512, 197, 768)
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous() # context_layer(512, 197, 12, 64)
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(*new_context_layer_shape)
        # MLP全链接层 self.out(Linear(in_features=768, out_features=768, bias=True))
        attention_output = self.out(context_layer) # attention_output(512, 197, 768)
        attention_output = self.proj_dropout(attention_output)
        return attention_output, weights


class Mlp(nn.Module):
    def __init__(self, config):
        super(Mlp, self).__init__()
        self.fc1 = Linear(config.hidden_size, config.transformer["mlp_dim"])
        self.fc2 = Linear(config.transformer["mlp_dim"], config.hidden_size)
        self.act_fn = ACT2FN["gelu"]
        self.dropout = Dropout(config.transformer["dropout_rate"])

        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.fc1.weight)
        nn.init.xavier_uniform_(self.fc2.weight)
        nn.init.normal_(self.fc1.bias, std=1e-6)
        nn.init.normal_(self.fc2.bias, std=1e-6)

    def forward(self, x):
        x = self.fc1(x)
        x = self.act_fn(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        return x


class Embeddings(nn.Module):
    """Construct the embeddings from patch, position embeddings.
    """
    def __init__(self, config, img_size, in_channels=3):
        super(Embeddings, self).__init__()
        self.hybrid = None
        img_size = _pair(img_size)

        if config.patches.get("grid") is not None:
            grid_size = config.patches["grid"]
            patch_size = (img_size[0] // 16 // grid_size[0], img_size[1] // 16 // grid_size[1])
            n_patches = (img_size[0] // 16) * (img_size[1] // 16)
            self.hybrid = True
        else:
            patch_size = _pair(config.patches["size"]) # wzw patch_size(16,16):卷积核大小kernel_size(16*16), 表示16*16的区域, 卷积出来一个特征
            n_patches = (img_size[0] // patch_size[0]) * (img_size[1] // patch_size[1]) # wzw n_patches(14*14): 一幅图片得到几个特征, 即序列长度(196), 图片大小224*224/卷积核大小16*16 = 14*14 ==> 划分成多少个14*14个部分(最终的多少个序列)(196)
            self.hybrid = False

        if self.hybrid:
            self.hybrid_model = ResNetV2(block_units=config.resnet.num_layers,
                                         width_factor=config.resnet.width_factor)
            in_channels = self.hybrid_model.width * 16
        # wzw, 构造卷积层, 用来将图片, 处理成embedding序列特征, Conv2d(3, 768, kernel_size=(16, 16), stride=(16, 16))
        # wzw, out_channel, 得到一个768dim的embedding(特征), 结合n_patches, 整个图片会得到(196, 768)的序列特征.
        self.patch_embeddings = Conv2d(in_channels=in_channels, # wzw, RGB:3个通道
                                       out_channels=config.hidden_size, # wzw, 卷积核个数(768), 表示每个区域卷积出来的特征是768dim.
                                       kernel_size=patch_size, # wzw, 卷积核大小(16,16)
                                       stride=patch_size) # wzw, stride:(16,16), 不重叠, 即得到n_patches个特征

        # wzw, 位置编码(1, 197, 768), 序列长度之所以不是196, 是因为多包含了一个cls_token(收作业的)
        self.position_embeddings = nn.Parameter(torch.zeros(1, n_patches+1, config.hidden_size))
        # wzw, (1,1,768), 和卷积得到的特征维度相同.
        self.cls_token = nn.Parameter(torch.zeros(1, 1, config.hidden_size))

        # wzw, 全链接层一般都会加一个dropout
        self.dropout = Dropout(config.transformer["dropout_rate"])

    def forward(self, x): # wzw, x输入图像 (512, 3, 224, 224)
        B = x.shape[0] # wzw, batch_size
        # wzw, 复制batch_size个. batch有512个instance, 每个instance都需要一个cls_token
        # wzw, 复制后,cls_tokens (1, 1, 768) -> (512, 1, 768)
        cls_tokens = self.cls_token.expand(B, -1, -1)

        if self.hybrid:
            x = self.hybrid_model(x)
        # wzw, 卷积, Conv2d(3, 768, kernel_size=(16,16), stride=(16,16))
        # wzw, 原始图片经过卷积得到特征图,, x (512, 3, 224, 224) -> (512, 768, 14, 14)
            # wzw, 14, 14 横向切割14个部分, 纵向切割乘14个部分, 14*14=196, 一个图片被切割成196个部分
        x = self.patch_embeddings(x)
        # wzw, 将特征图展开, 得到序列 (512, 768, 196)
        x = x.flatten(2) # wzw, 从第3个维度开始展开, 14*14=60
        # wzw, 调换维度 x (512, 196, 768)
        x = x.transpose(-1, -2)
        # wzw, 在序列中, 加入cls_token (512, 1, 768), 拼接到第二个维度(序列长度).
        # wzw, 此时x(512, 196, 768) -> (512, 197, 768) 序列长度多了一个
        x = torch.cat((cls_tokens, x), dim=1)

        # wzw, 位置编码 (1, 197, 768), 对于batch中的instance, position_encoding都是一样的.
        embeddings = x + self.position_embeddings
        embeddings = self.dropout(embeddings)
        return embeddings


class Block(nn.Module):
    def __init__(self, config, vis):
        super(Block, self).__init__()
        self.hidden_size = config.hidden_size
        self.attention_norm = LayerNorm(config.hidden_size, eps=1e-6) # wzw, LayerNorm
        self.ffn_norm = LayerNorm(config.hidden_size, eps=1e-6) # wzw, LayerNorm
        self.ffn = Mlp(config) # wzw, MLP
        self.attn = Attention(config, vis) # Attention(QKV)

    def forward(self, x):
        h = x
        # wzw, layerNorm
        x = self.attention_norm(x)
        # wzw, Attention
        x, weights = self.attn(x)
        # wzw, 残差相加(
        x = x + h

        h = x
        # wzw, LayNorm
        x = self.ffn_norm(x)
        # wzw, MLP
        x = self.ffn(x)
        x = x + h
        return x, weights

    def load_from(self, weights, n_block):
        ROOT = f"Transformer/encoderblock_{n_block}"
        with torch.no_grad():
            query_weight = np2th(weights[pjoin(ROOT, ATTENTION_Q, "kernel")]).view(self.hidden_size, self.hidden_size).t()
            key_weight = np2th(weights[pjoin(ROOT, ATTENTION_K, "kernel")]).view(self.hidden_size, self.hidden_size).t()
            value_weight = np2th(weights[pjoin(ROOT, ATTENTION_V, "kernel")]).view(self.hidden_size, self.hidden_size).t()
            out_weight = np2th(weights[pjoin(ROOT, ATTENTION_OUT, "kernel")]).view(self.hidden_size, self.hidden_size).t()

            query_bias = np2th(weights[pjoin(ROOT, ATTENTION_Q, "bias")]).view(-1)
            key_bias = np2th(weights[pjoin(ROOT, ATTENTION_K, "bias")]).view(-1)
            value_bias = np2th(weights[pjoin(ROOT, ATTENTION_V, "bias")]).view(-1)
            out_bias = np2th(weights[pjoin(ROOT, ATTENTION_OUT, "bias")]).view(-1)

            self.attn.query.weight.copy_(query_weight)
            self.attn.key.weight.copy_(key_weight)
            self.attn.value.weight.copy_(value_weight)
            self.attn.out.weight.copy_(out_weight)
            self.attn.query.bias.copy_(query_bias)
            self.attn.key.bias.copy_(key_bias)
            self.attn.value.bias.copy_(value_bias)
            self.attn.out.bias.copy_(out_bias)

            mlp_weight_0 = np2th(weights[pjoin(ROOT, FC_0, "kernel")]).t()
            mlp_weight_1 = np2th(weights[pjoin(ROOT, FC_1, "kernel")]).t()
            mlp_bias_0 = np2th(weights[pjoin(ROOT, FC_0, "bias")]).t()
            mlp_bias_1 = np2th(weights[pjoin(ROOT, FC_1, "bias")]).t()

            self.ffn.fc1.weight.copy_(mlp_weight_0)
            self.ffn.fc2.weight.copy_(mlp_weight_1)
            self.ffn.fc1.bias.copy_(mlp_bias_0)
            self.ffn.fc2.bias.copy_(mlp_bias_1)

            self.attention_norm.weight.copy_(np2th(weights[pjoin(ROOT, ATTENTION_NORM, "scale")]))
            self.attention_norm.bias.copy_(np2th(weights[pjoin(ROOT, ATTENTION_NORM, "bias")]))
            self.ffn_norm.weight.copy_(np2th(weights[pjoin(ROOT, MLP_NORM, "scale")]))
            self.ffn_norm.bias.copy_(np2th(weights[pjoin(ROOT, MLP_NORM, "bias")]))


class Encoder(nn.Module):
    def __init__(self, config, vis):
        super(Encoder, self).__init__()
        self.vis = vis
        # wzw, 共有12层
        self.layer = nn.ModuleList()
        # wzw, LN(LayerNormalization), 对一个instance进行归一化, BN(BatchNormalization)则是对多个batch的同一位置进行归一化
        self.encoder_norm = LayerNorm(config.hidden_size, eps=1e-6) # wzw, hidden_size(768)
        # wzw, num_layers:12, 一共有12层
        for _ in range(config.transformer["num_layers"]):
            layer = Block(config, vis)
            self.layer.append(copy.deepcopy(layer))

    def forward(self, hidden_states): # hidden_states:(embedding层得到的序列特征 (512, 197, 768) )
        attn_weights = []
        for layer_block in self.layer:
            # layer_block: 对得到的序列特征, 通过self-attention 进一步提取特征.
            hidden_states, weights = layer_block(hidden_states)
            if self.vis:
                attn_weights.append(weights)
        encoded = self.encoder_norm(hidden_states)
        return encoded, attn_weights


class Transformer(nn.Module):
    def __init__(self, config, img_size, vis):
        super(Transformer, self).__init__()
        # wzw, 卷积层, 构造序列特征
            # Conv2d(3, 768, kernel_size=(16,16), stride=(16,16)), 输入彩色图RGB, 输出768dim向量
        # wzw, 经过Embedding, self.embedding (512, 197, 768) 得到一个batch的序列特征
        self.embeddings = Embeddings(config, img_size=img_size)
        # wzw, self-attention, 把注意力加进去
        self.encoder = Encoder(config, vis)

    def forward(self, input_ids):
        embedding_output = self.embeddings(input_ids)
        encoded, attn_weights = self.encoder(embedding_output)
        return encoded, attn_weights


class VisionTransformer(nn.Module):
    def __init__(self, config, img_size=224, num_classes=21843, zero_head=False, vis=False):
        super(VisionTransformer, self).__init__()
        self.num_classes = num_classes
        self.zero_head = zero_head
        self.classifier = config.classifier

        self.transformer = Transformer(config, img_size, vis)
        self.head = Linear(config.hidden_size, num_classes)

    def forward(self, x, labels=None): # wzw, x:(512, 3, 224, 224), 输入数据
        x, attn_weights = self.transformer(x) # 得到特征 x(512, 197, 768), attn_weights(512, 12, 197, 197)
        # wzw, 10分类. self.head(Linear(in_features=768, out_features=10, bias=True))
        # logits(512,768), 取每个batch的cls_token(768dim)取计算logits
        logits = self.head(x[:, 0]) # x[:, 0], 表示所有的batch都要(512个instance), 0表示针对batch中的每个instance(197*768)只取序列的第一个位置(cls_token 768dim)

        if labels is not None:
            loss_fct = CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_classes), labels.view(-1))
            return loss
        else:
            return logits, attn_weights

    def load_from(self, weights):
        with torch.no_grad():
            if self.zero_head:
                nn.init.zeros_(self.head.weight)
                nn.init.zeros_(self.head.bias)
            else:
                self.head.weight.copy_(np2th(weights["head/kernel"]).t())
                self.head.bias.copy_(np2th(weights["head/bias"]).t())

            self.transformer.embeddings.patch_embeddings.weight.copy_(np2th(weights["embedding/kernel"], conv=True))
            self.transformer.embeddings.patch_embeddings.bias.copy_(np2th(weights["embedding/bias"]))
            self.transformer.embeddings.cls_token.copy_(np2th(weights["cls"]))
            self.transformer.encoder.encoder_norm.weight.copy_(np2th(weights["Transformer/encoder_norm/scale"]))
            self.transformer.encoder.encoder_norm.bias.copy_(np2th(weights["Transformer/encoder_norm/bias"]))

            posemb = np2th(weights["Transformer/posembed_input/pos_embedding"])
            posemb_new = self.transformer.embeddings.position_embeddings
            if posemb.size() == posemb_new.size():
                self.transformer.embeddings.position_embeddings.copy_(posemb)
            else:
                logger.info("load_pretrained: resized variant: %s to %s" % (posemb.size(), posemb_new.size()))
                ntok_new = posemb_new.size(1)

                if self.classifier == "token":
                    posemb_tok, posemb_grid = posemb[:, :1], posemb[0, 1:]
                    ntok_new -= 1
                else:
                    posemb_tok, posemb_grid = posemb[:, :0], posemb[0]

                gs_old = int(np.sqrt(len(posemb_grid)))
                gs_new = int(np.sqrt(ntok_new))
                print('load_pretrained: grid-size from %s to %s' % (gs_old, gs_new))
                posemb_grid = posemb_grid.reshape(gs_old, gs_old, -1)

                zoom = (gs_new / gs_old, gs_new / gs_old, 1)
                posemb_grid = ndimage.zoom(posemb_grid, zoom, order=1)
                posemb_grid = posemb_grid.reshape(1, gs_new * gs_new, -1)
                posemb = np.concatenate([posemb_tok, posemb_grid], axis=1)
                self.transformer.embeddings.position_embeddings.copy_(np2th(posemb))

            for bname, block in self.transformer.encoder.named_children():
                for uname, unit in block.named_children():
                    unit.load_from(weights, n_block=uname)

            if self.transformer.embeddings.hybrid:
                self.transformer.embeddings.hybrid_model.root.conv.weight.copy_(np2th(weights["conv_root/kernel"], conv=True))
                gn_weight = np2th(weights["gn_root/scale"]).view(-1)
                gn_bias = np2th(weights["gn_root/bias"]).view(-1)
                self.transformer.embeddings.hybrid_model.root.gn.weight.copy_(gn_weight)
                self.transformer.embeddings.hybrid_model.root.gn.bias.copy_(gn_bias)

                for bname, block in self.transformer.embeddings.hybrid_model.body.named_children():
                    for uname, unit in block.named_children():
                        unit.load_from(weights, n_block=bname, n_unit=uname)


CONFIGS = {
    'ViT-B_16': configs.get_b16_config(),
    'ViT-B_32': configs.get_b32_config(),
    'ViT-L_16': configs.get_l16_config(),
    'ViT-L_32': configs.get_l32_config(),
    'ViT-H_14': configs.get_h14_config(),
    'R50-ViT-B_16': configs.get_r50_b16_config(),
    'testing': configs.get_testing(),
}
