#! /usr/bin/env bash

# 执行命令: ./005_position_args.sh --flag pos1 --flag pos2

echo "number of position args: $#"

echo "position args: $@"
echo "position args: $*"

# remove two position args
echo ">>>> shift 2"
shift 2


echo "number of position args: $#"

echo "position args: $@"
echo "position args: $*"
