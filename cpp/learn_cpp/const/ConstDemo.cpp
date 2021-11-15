//
// Created by wuzewei.wzw on 2021/11/15.
//

#include "ConstDemo.h"

// define member function outside class definition: use ClassName:: as prefix
std::string ConstDemo::const_member_func() const {
    return const_member_name;
}
