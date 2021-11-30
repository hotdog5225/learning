//
// Created by wuzewei.wzw on 2021/11/30.
//

#include <iostream>

class Person {
public:
    int m_age{};
    std::string m_name{};

    // has default value, so "default constructor" can be omitted
    Person(const std::string &name = "", int age = 0) : m_age{age}, m_name{name} {};

    const std::string &get_name() const {
        return m_name;
    }

    int get_age() const {
        return m_age;
    }

};

class BaseballPlayer: public Person {
public:
    double m_battingAverage{};
    int m_homeRuns{};

    // has default value, so "default constructor" can be omitted
    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0): m_battingAverage{battingAverage}, m_homeRuns{homeRuns} {};
};

int main() {
    BaseballPlayer b{};
    b.m_name = "hotdog";
    std::cout << b.get_name() << std::endl;
}