//计算两个数的和
const CryptoJS = require("crypto-js");

function add(num1, num2) {
    return num1 + num2;
}

function my_ecrypt(orimsg) {
    var CryptoJS = require("crypto-js");
    var aseKey = "imed2019imed2019"     // js中写死的
    var message = orimsg;

//加密
    var encrypt = CryptoJS.AES.encrypt(message, CryptoJS.enc.Utf8.parse(aseKey), {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }).toString();
    encrypt = encrypt.replace(/\+/gi, "-"),
        encrypt = encrypt.replace(/\//gi, "_"),
        encrypt;
    console.log("加密后: ", encrypt);

    return encrypt
}

function my_decrypt(encrypt_msg) {
    var CryptoJS = require("crypto-js");
    var aseKey = "imed2019imed2019"     // js中写死的
    var message = encrypt_msg;

    message = message.replace(/-/gi, "+"),
        message = message.replace(/_/gi, "/"),
        message;

//解密
    var decrypt = CryptoJS.AES.decrypt(encrypt, CryptoJS.enc.Utf8.parse(aseKey), {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }).toString(CryptoJS.enc.Utf8);
    console.log(decrypt);
    
    return decrypt
}

//新增一个导出函数（node方式）
module.exports.init = function (arg1, arg2) {
    //调用函数，并返回
    console.log(add(arg1, arg2));
};

// 加密函数
module.exports.my_encrypt = function (ori_msg) {
    return my_ecrypt(ori_msg)
}

// 解密函数
module.exports.my_decrypt = function (encrypt_msg) {
    return my_ecrypt(encrypt_msg)
}
