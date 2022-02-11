//
// Created by wuzewei.wzw on 2022/1/31.
//

#include <iostream>

#ifndef LEARN_CPP_TEST_CONST_H
#define LEARN_CPP_TEST_CONST_H

// const default is internal linkage, cannot be accessed in other file (e.g. test_const_2.h)
const int const_a = 10;

// 'extern' make const external linkage, can be accessed in other file(e.g. test_const2.h)
extern const int const_b = 100;

#endif //LEARN_CPP_TEST_CONST_H
