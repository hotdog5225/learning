#! /usr/bin/env bash

# 变量赋值

    # ${a-value} a没有被设定(unset)时,返回后面的值. 同时不会给a赋值(a仍为unset)
        new_value='new value'

        a=; # set a=null 空值
        echo ">>> next line will print nothing, bacause a is set to null, not unset"
        echo ${a-"${new_value}"} 

        unset a # 此时a被unset(未设置)
        echo ">>> next line will print 'new value', bacause a is unset"
        echo ${a-"${new_value}"} 
        echo ">>> next line will print nothing, bacause a is not assigned"
        echo ${a}

    # : 表示null(空值)会被考虑进去

    # #{b:-value} b没有被设定 or b为空值(null)时, 返回后面的值(value). b不会被赋值
        b=; # set b=null 空值
        echo ">>> next line will print 'new value', because b is null, satisfy contidion 'unset or null'" 
        echo ${b:-"${new_vblue}"} 
        echo ">>> next line will print nothing, because b is not assigned"
        echo ${b}

    # ${a=value} 和 ${a-value}一样, 只不过多了一个赋值操作.
    # ${a:=value} 和 ${a:-value}一样, 只不过多了一个赋值操作.

