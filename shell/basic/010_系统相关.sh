#! /usr/bin/env bash

# 日期相关

	# 按照%Y%m%d的格式, 输出20211223的前一天的日期
	# date +%Y%m%d -d "-1 day 20211223" 



# 目录相关

	# dirname 删除最后一个"非/部分 & 尾随的/"
	echo ">>>> dirname 示例"
	dirname "user/name/" # user
	dirname "name/" # .

	# 常用于在脚本中, 获取脚本的父目录
	dirname $0 # ./basic

	# 获取脚本的绝对路径
	cd `dirname $0`; pwd # /Users/wuzewei.wzw/Documents/learning/shell/basic
	# 获取软连接的绝对路径
	echo $(readlink $0)
	cd `dirname $(readlink $0)` ; pwd