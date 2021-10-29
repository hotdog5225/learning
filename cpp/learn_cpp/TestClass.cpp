#include "TestClass.h"

// define member function outside class definition: use ClassName:: as prefix
std::string TestClass::get_name() const {
    return m_name;
}

const std::string &TestClass::get_const_ref_to_member() const {
    return m_name;
}

// static member definition, not subject to access control
int TestClass::age = 18;

// static member function, used to access static member.
// and static member function can only access other static member/function.
int TestClass::get_private_staic_member() {
    return age;
}
