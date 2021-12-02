//
// Created by wuzewei.wzw on 2021/11/30.
//

#include <iostream>

class Base {
public:
    int m_age{};

    // has default value, so "default constructor" can be omitted
    Base(int age = 0) : m_age{age} {
        std::cout << "initialize Base" << std::endl;
    };

    int get_age() const {
        return m_age;
    }

};

class Derived : public Base {
public:
    double m_salary{};

    // has default value, so "default constructor" can be omitted
    Derived(double salary = 0.0) : m_salary{salary} {
        std::cout << "initialize Derived" << std::endl;
    };
};

int main() {
    // when c++ construct a Class object, it constructs object according to the inheritance tree
    Derived d{};
    /*
     * initialize Base
     * initialize Derived
     */
}