#include <iostream>
#include <memory>
#include <string>
#include <unordered_set>
#include <map>
#include <functional>

#include "TestClass.h"

int main() {

    // call default constructor (supplied by compiler)
    TestClass non_const_t{};

    // const , reference, pointer

    // reference to const(常量引用): const &
    int non_const_var = 2;
    // must be initialized when define
    const int &ref_to_const = non_const_var; // 常量引用可以绑定non-const对象
    std::cout << "[ref_to_const bind a non_const var]: " << std::to_string(ref_to_const) << '\n';

    // pointer to const(指向常量的指针): const * (从右向左读, 首先是一个指针, 然后指向一个const)
    // can be uninitialized when defined
    const int *pointer_to_const; // 指向常量的指针, 可以指向non-const对象
    pointer_to_const = &non_const_var;
    std::cout << "[pointer_to_const points to a non_const var]: " << std::to_string(*pointer_to_const) << '\n';
    // can change to point another var
    int non_const_var_2 = 3;
    pointer_to_const = &non_const_var_2;

    // const pointer: * const (从右向左读: 首先是一个const, 类型是一个指针)
    int *const const_pointer = &non_const_var;
    // can change the object it points to
    *const_pointer = 4;
    // can not change to point another object: because the pointer itself is a Const object.
    // const_pointer = &non_const_var_2;

    /*------------------*/

    // auto 总会推导出一个"值类型", 绝对不会是引用类型
    auto &test = non_const_t.get_const_ref_to_member(); // const function can only return 'const reference' to member, if ref is returned
    // test = "test"; // can not change member, for test is a const reference

    auto &test2 = non_const_t.get_ref_to_member(); // non-const function can return 'reference' to member
    test2 = "test"; // can change member from the caller
    std::cout << "[member has been changed: function return reference to member] \n" << std::endl;


    return 0;
}