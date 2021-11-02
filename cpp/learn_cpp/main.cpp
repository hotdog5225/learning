#include <iostream>
#include <memory>
#include <string>
#include <unordered_set>
#include <map>
#include <functional>

#include "TestClass.h"

template<typename T>
// template type declaration
T sya_hello(T a) {
    std::cout << "[template function] called: " << a << '\n' << std::endl;
    return a;
}

// used for std::bind
void test_func(int a) {
    std::cout << "[std::bind] : " << a << '\n' << std::endl;
}

int main() {
    // call default constructor
    TestClass t1{}; // list initialization(with empty brace): will do "value initialization, init member to zero". better than TestClass t1(default initialization);
    // call according constructor
    TestClass non_const_t2{"hotdog5225"}; // list initialization : call according constructor

    /*------------------*/

    // define a member function outside the class.
    std::cout << "[member func called: ]" << non_const_t2.get_name() + '\n' << std::endl;

    /*------------------*/

    // const class object can only call const member function. any manner change member is not allowed
    const TestClass const_t3{"const_class"};
    std::cout << "[const member function called] " << const_t3.get_name() << std::endl;

    // non-const class object can also call const function
    std::cout << "[const member func called by non-const object]" << non_const_t2.get_name() + '\n' << std::endl;

    /*------------------*/

    // template function called
    sya_hello(3);

    /*------------------*/

    // std::bind
    auto f = std::bind(test_func, std::placeholders::_1);
    f(1);

    /*------------------*/

    // call according Constructor, and initiate const member with member initializer list.
    TestClass non_const_t4{"hotdog", "hotdog_const"};

    // non-const class object can call const member function
    non_const_t4.get_name();

    // auto 总会推导出一个值类型, 绝对不会是引用类型
    /*
    auto& test = non_const_t4.get_const_ref_to_member(); // const function can only return 'const reference' to member
    test = "test"; // can not change member
     */
    auto &test2 = non_const_t4.get_ref_to_member(); // non-const function can return 'reference' to member
    test2 = "test"; // can change member from the caller
    std::cout << "[member has been changed: function return reference to member] \n" << std::endl;

    /*------------------*/

    // initialize static member vector<int>
    // call static member directly by Class
    std::cout << "[call static member through Class]: ";
    for (const auto int_member : TestClass::static_vec) {
        std::cout << std::to_string(int_member) << ", ";
    }
    std::cout << '\n';

    return 0;
}