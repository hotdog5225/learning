//
// Created by wuzewei.wzw on 2022/1/31.
//

#include <iostream>

#ifndef LEARN_CPP_TEST_CONST_2_H
#define LEARN_CPP_TEST_CONST_2_H

std::cout << const_a << std::endl;

// user extern to declare const_b is defined in other file( test_const.h)
extern const int const_b;
std::cout << const_b << std::endl;

#endif //LEARN_CPP_TEST_CONST_2_H
