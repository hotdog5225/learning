import argparse

# https://docs.python.org/zh-cn/3/howto/argparse.html tutorial

# 执行命令: python argparse_learn.py 4 --verbosity 1
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # 位置参数(必选)
    parser.add_argument("square", help="square given number", type=int)

    # 可选参数
    parser.add_argument("-v", "--verbosity", help="increase output verbosity")
        # store_true表示只会是true or false. 不用指定具体的值.
        # 执行命令: python argparse_learn.py 4 --verbosity
    # parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")

    # 解析命令行, 获取位置/可选参数
    args = parser.parse_args()

    result = args.square ** 2 # 位置参数不指定不会为none, 所以命令行中不可省略.

    if args.verbosity: # 可选参数, 命令行中不指定默认为none, 可作为条件
        print("square of given number is : %s" % result)
    else:
        print(result)