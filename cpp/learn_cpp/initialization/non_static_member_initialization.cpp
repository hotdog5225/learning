//
// Created by wuzewei.wzw on 2022/4/11.
//

#include <iostream>

class NonStaticMemberInitialization {
private:
    // "Non-static member initialization" / "in-class member initializers"
    double _x{1.0}; // 可以"直接"为"non-static" class member提供一个默认值
public:
    // 默认构造函数
    NonStaticMemberInitialization() {};// 因为没有"member initialization list", 给member提供初始化值, 所以采用默认值进行初始化. 这里就是 _x==>1.0

    void print() {
        std::cout << _x << std::endl;
    }
};

int main() {
    NonStaticMemberInitialization n{}; // 调用默认构造函数
    n.print();

    return 0;
}

// g++ --std=c++11 non_static_member_initialization.cpp