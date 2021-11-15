#include "TestClass.h"

// static member "definition", not subject to access control
int TestClass::age = 18;

// static member function, used to access static member.
// and static member function can only access other static member/function.
int TestClass::get_private_static_member() {
    return age;
}

// use lambda to init static member
std::vector<int> TestClass::static_vec {
        []() {
            std::vector<int> tmp_vec = {1,2,3,4};
            return tmp_vec;
        }() // do not lose "()", call the lambda right away!
};
