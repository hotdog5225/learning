#include "TestClass.h"

const std::string &TestClass::get_const_ref_to_member() const {
    return m_name;
}
