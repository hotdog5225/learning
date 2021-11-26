//
// Created by wuzewei.wzw on 2021/11/15.
//

#include "TestClass.h"
#include "IntArray.h"

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
    for (const auto int_member: TestClass::static_vec) {
        std::cout << std::to_string(int_member) << ", ";
    }
    std::cout << '\n';

    /*------------------*/

    // static function called, use Class Name as prefix
    std::cout << TestClass::get_private_static_member() << std::endl;

    /*------------------*/

    // use list initialization to initialize IntArray(customer object)
    IntArray ia{1, 2, 3, 4, 5};
//    ia.printArray();

    // use  list assignment to initialize IntArray(customer objcet)
    IntArray ia2 = {10, 9, 8, 7};
//    ia2.printArray();

    return 0;
}