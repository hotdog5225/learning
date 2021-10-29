#pragma once

#include <iostream>

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

    // members can not be changed in this const member function
    // const function can be called both by const & non-const class object
    std::string get_name() const;

    // const member function can only return const reference to member (if reference is returned)
    // in this way, the caller can not change the member returned.
    const std::string &get_const_ref_to_member() const;

    // non-const member function can return reference to member
    // so the non-const object(caller) can change member's value.
    std::string &get_ref_to_member() {
        return m_name;
    }

    // static member function, used to access private static member, with no need to instantiate an object!
    // and static member function can only access other static member/function.
    static int get_private_staic_member();

private:
    std::string m_name{}; // should always init member by initialization list
    const std::string m_const_name{}; // const member, never can be changed

    // static subject to class , not object
    // can be directly accessed by Class:: (if public)
    // must be defined out of class, in the global scope
    // static member definition not subject to Access Ctrl, just definition! object can not access it directly if it's private!
    static int age;
};
