#pragma once

#include <iostream>
#include <vector>

class TestClass {
public:
    // const member function can only return const reference to member (if reference is returned)
    // in this way, the caller can not change the member returned.
    const std::string &get_const_ref_to_member() const;

    // non-const member function can return reference to member
    // so the non-const object(caller) can change member's value.
    std::string &get_ref_to_member() {
        return m_name;
    }

private:
    std::string m_name{}; // should always init member by initialization list
};
