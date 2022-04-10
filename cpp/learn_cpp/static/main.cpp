//
// Created by wuzewei.wzw on 2022/4/10.
//

#include <iostream>

class StaticLearn {
private:
    // just forward declaration, 不能在这里定义
    // static member更像是全局变量, 在程序开始的时候就需要被初始化. 所以必须被显示的在类外进行定义.(global scope)
    // static member 和 object没有任何关系.
    static int static_a;
public:
    // 需要实例化一个object, 去访问static member variable
    void print() {
        // 因为是程序开始时就初始化的, 所以这里当然可以使用
        std::cout << StaticLearn::static_a << std::endl;
    }

    // 无需实例化object, 通过ClassName去访问静态成员变量
    static int read_static() {
        return static_a;
    }
};

// 虽然static_a是private的, 但是仍然可以定义, 初始化不受access control影响
// 既然是定义, 不要忘记了"int"
int StaticLearn::static_a{10}; // list initialization

int main() {
    // 实例化一个object去访问static member variable
    StaticLearn s;
    s.print();

    // 通过static member func去访问 static member variable
    std::cout << StaticLearn::read_static() << std::endl;
}