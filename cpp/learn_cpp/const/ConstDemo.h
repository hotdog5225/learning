//
// Created by wuzewei.wzw on 2021/11/15.
//

#ifndef LEARN_CPP_CONSTDEMO_H
#define LEARN_CPP_CONSTDEMO_H


#include <iostream>

class ConstDemo {
public:
    ConstDemo(std::string name) : const_member_name(name) {} // member initializer list : initialize member, not assign

    // const member function
    // members can not be changed in this const member function
    // const function can be called both by const & non-const class object
    std::string const_member_func() const;

private:
    std::string const_member_name{};
};


#endif //LEARN_CPP_CONSTDEMO_H
