#pragma once

#include <iostream>
#include <vector>

class TestClass {
public:
    TestClass() = default; // more safe than the TestClass() {}; will initialize member to zero-value (if no initializer provided in the declaration)

    TestClass(std::string name) : m_name{name} { // member initializer list : initialize member, not assign
        std::cout << "[user defined Constructor called]" << std::endl;
    };

    TestClass(std::string name, const std::string const_name) : m_name{name}, m_const_name{
            const_name} { // initialize a const member, not assign
        std::cout << "[user defined Constructor called] with const_member initialized!" << std::endl;
    };

    ~TestClass() { // no need for fundamental type (e.g. here)
        std::cout << "[user defined Destructor called]" << std::endl;
    };

    // static member function, used to access private static member, with no need to instantiate an object!
    // and static member function can only access other static member/function.
    static int get_private_static_member();

    static std::vector<int> static_vec;

private:
    std::string m_name{}; // should always init member by initialization list
    const std::string m_const_name{}; // const member, never can be changed

    // static subject to class , not object
    // can be directly accessed by Class:: (if public)
    // must be defined out of class, in the global scope
    // static member definition not subject to Access Ctrl, just definition! object can not access it directly if it's private!
    static int age;
};
