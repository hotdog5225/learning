//
// Created by wuzewei.wzw on 2021/11/30.
//

#include <iostream>

class Base {
private:
    int m_age{};

public:
    // has default value, so "default constructor" can be omitted
    Base(int age = 0) : m_age{age} {
        std::cout << "initialize Base" << std::endl;
    };

    int get_age() const {
        return m_age;
    }

};

class Derived : public Base {
private:
    double m_salary{};

public:
    // has default value, so "default constructor" can be omitted
    Derived(double salary = 0.0) : m_salary{salary} {
        std::cout << "initialize Derived" << std::endl;
    };

    // specify which constructor of Base is called
    Derived(double salary, int age) : Base(age), m_salary{salary} {};

    double get_salary() {
        return m_salary;
    }
};

int main() {
    // when c++ construct a Class object, it constructs object according to the inheritance tree
    // first Base, then Derived
    Derived d{};
    /*
     * initialize Base
     * initialize Derived
     */

    // initialize Base members, when constructor of Derived is called
    Derived d2{100.0, 18};
    std::cout << d2.get_salary() << std::endl;
    std::cout << d2.get_age() << std::endl;

}