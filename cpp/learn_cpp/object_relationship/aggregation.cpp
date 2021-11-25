//
// Created by wuzewei.wzw on 2021/11/25.
//
#include <iostream>
#include <vector>

class Teacher {
private:
    std::string m_name{};

public:
    Teacher() = default;

    Teacher(const std::string &name) : m_name{name} {};

    const std::string &get_name() const {
        return m_name;
    }
};

class Department {
private:
    const Teacher &m_teacher;

    // when we want to contain multi other objects, we may use std::vector or other std lib lists.
    // but fixed array and various std lib lists can't hold reference (because list elements must be assignable, but references can't be assigned)
    // instead of reference, we can use pointer, but that would open the possibility to store and pass "null pointer"
    // so, if null pointer is not allowed,  we use "std::reference_wrapper", which is a class, and act like a reference
    std::vector <std::reference_wrapper<const Teacher>> m_teacher_list;// if we need a const reference, we need to add "const" before Teacher

public:
    Department(const Teacher &teacher) : m_teacher{teacher} {};

    // append a teacher to m_teacher_list
    std::vector <std::reference_wrapper<const Teacher>> registerTeacher(Teacher t) {
        m_teacher_list.push_back(t);
        return m_teacher_list;
    }
};

int main() {
    Teacher t{"hotdog"};

    {
        Department d1 = {t};
        std::vector <std::reference_wrapper<const Teacher>> teacherList = d1.registerTeacher(t);
        for (auto t: teacherList) {
            // use t.get() to get reference
            std::cout << t.get().get_name() << std::endl;
        }
    }

}
