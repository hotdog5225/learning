//
// Created by wuzewei.wzw on 2021/11/26.
//

#ifndef LEARN_CPP_INTARRAY_H
#define LEARN_CPP_INTARRAY_H

#include <cassert> // for assert
#include <initializer_list> // for std::initializer_list

class IntArray {
private:
    int m_length{}; // 0
    int *m_data{}; // 0x0

public:
    IntArray() = default;

    explicit IntArray(int length) :
            m_length{length},
            m_data{new int[length]{}} {};

    // for enabling list initialization "IntArray ia {xxx, xxx, xxx}"
    IntArray(std::initializer_list<int> list) // allow IntArray to be initialized via list initialization (take a std::initializer_list as argument)
            : IntArray(static_cast<int>(list.size())) { // use delegating constructor to set up initial array

        int idx{0};
        for (auto ele: list) {
            m_data[idx] = ele;
            idx++;
        }
    }

    // for enabling list assignment "IntArray ia = {xx, xx, xx}"
    IntArray &operator=(std::initializer_list<int> list) {
        // if the new list is a different length, reallocate it
        int length{static_cast<int>(list.size())};
        if (length != m_length) {
            delete[] m_data;
            m_length = length;
            m_data = new int[m_length]{};
        }

        // initialize IntArray from the list
        int idx{0};
        for (auto ele: list) {
            m_data[idx] = ele;
            idx++;
        }

        return *this;
    }

    ~IntArray() {
        delete[] m_data;
    }

    int &operator[](int idx) {
        assert(idx >= 0 && idx < m_length);
        return m_data[idx];
    }

    void printArray() {
        for (int i = 0; i < m_length; ++i) {
            std::cout << m_data[i] << std::endl;
        }
    }

};

#endif //LEARN_CPP_INTARRAY_H
