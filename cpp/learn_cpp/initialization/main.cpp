//
// Created by wuzewei.wzw on 2021/11/15.
//

#include "TestClass.h"

int main() {
    // call default constructor
    TestClass non_const_t1{}; // list initialization(with empty brace): will do "value initialization, init member to zero". better than TestClass non_const_t1(default initialization);

    // call according constructor
    TestClass non_const_t2{"hotdog5225"}; // list initialization : call according constructor

    // call according Constructor, and initiate const member with "member initializer list".
    TestClass non_const_t3{"hotdog", "hotdog_const"};

    /*------------------*/

    // initialize static member vector<int>
    // call static member directly by Class
    std::cout << "[call static member through Class]: ";
    for (const auto int_member : TestClass::static_vec) {
        std::cout << std::to_string(int_member) << ", ";
    }
    std::cout << '\n';

    /*------------------*/

    // static function called, use Class Name as prefix
    std::cout << TestClass::get_private_static_member() << std::endl;

    return 0;
}