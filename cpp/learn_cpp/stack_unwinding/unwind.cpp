//
// Created by wuzewei.wzw on 2022/5/15.
// 展示如何通过"栈展开", 避免"内存泄漏"
//

#include <iostream>

class Shape {
public:
    ~Shape() {
        std::cout << "Shape析构函数被调用, 内存已释放" << std::endl;
    }

};

class PtrWrapper {
public:
    PtrWrapper(Shape * ptr): ptr_{ptr} {}
    ~PtrWrapper() {
        std::cout << "栈展开: 自动调用栈变量的析构函数" << std::endl;
        delete ptr_; // 在析构函数中, 对内存进行清理.
    }
private:
    Shape * ptr_;
};

int main() {
    // 堆: 分配内存, 并构造一个Shape对象, 返回其指针.
    Shape * s = new Shape();

    // 为了防止内存泄漏, 不手动释放内存(delete s), 而是利用"栈展开"(会自动调用非POD的析构函数, 即使异常发生), 在本地变量的析构函数中, 进行内存清理.
    // ①将指针s保存到本地变量p中 (栈)
    PtrWrapper p(s);
    // ②本地变量p声明周期结束后, 自动调用p的析构函数==>释放s.

    return 0;
}

