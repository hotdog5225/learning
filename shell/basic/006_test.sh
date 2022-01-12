#! /usr/bin/env bash

# (()) 用于整型数字计算, 也可用于整数的逻辑运算
# use $ to get result of (())
echo $(( 3 > 2 )) # 1 , "true" 
echo $? # 0


# test exp or [ exp ]
# form1: []
if [ $# -lt 2 ]; then
	echo "need two command args"
fi
# form2: test
if test $# -lt 2; then
	echo "need two command args"
fi


# [[]]