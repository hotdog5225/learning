//
// Created by wuzewei.wzw on 2021/11/15.
//

#include "ConstDemo.h"

int main() {
    // const class object can only call const member function. any manner change member is not allowed
    const ConstDemo const_t{"const_class"};
    std::cout << "[const member function called by const object] " << const_t.const_member_func() << std::endl;

    // non-const class object can also call const function
    ConstDemo non_const_t{"non_const_class"};
    std::cout << "[const member func called by non-const object]" << non_const_t.const_member_func() << std::endl;

    return 0;
}