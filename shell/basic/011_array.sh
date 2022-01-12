#! /usr/bin/env bash

# 创建空数组
empty_arr=()

# 创建非空数组
arr=(1 "hello world")

# 数组添加元素
arr+=("new")

# 遍历数组
for item in ${arr[@]}; do
	echo $item
done
		# 1
		# hello world
