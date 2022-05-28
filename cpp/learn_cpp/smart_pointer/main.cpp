//
// Created by wuzewei.wzw on 2022/5/19.
//
#include <iostream>

class Shape {
public:
    ~Shape() {
//        std::cout << "call ~Shape()" << std::endl;
    }
};

template<typename T>
class SmartPtr {
public:
    // 利用栈展开, 防止内存泄漏
    ~SmartPtr() {
//        std::cout << "call ~SmartPtr()" << std::endl;
        delete ptr_;
    }

    // 默认构造函数
    SmartPtr() = default;

    // 自定义构造函数
    SmartPtr(T *ptr) : ptr_(ptr) {
//        std::cout << "自定义构造函数" << std::endl;
    }

//    // 拷贝构造函数
//    SmartPtr(SmartPtr &other) {
//        std::cout << "拷贝构造" << std::endl;
//        ptr_ = other.release();
//    }
//
    T* release() {
        T* ptr = ptr_;
        ptr_ = nullptr;
        return ptr;
    }

//    // 赋值运算符
//    SmartPtr& operator=(SmartPtr& rhs) {
//        std::cout << "赋值运算符" << std::endl;
//        SmartPtr(rhs).swap(*this);
//
//        return *this;
//    }

    // 移动构造函数
    SmartPtr(SmartPtr&& other) {
        std::cout << "移动构造" << std::endl;
        ptr_ = other.release();
    }

    // 赋值运算符
    SmartPtr& operator=(SmartPtr other) {
        std::cout << "赋值运算符" << std::endl;
        other.swap(*this);
        return *this;
    }

    void swap(SmartPtr& rhs) {
        std::cout << "swap" << std::endl;
        std::swap(ptr_, rhs.ptr_);
    }

    T *get() const { return ptr_; }

    // 解引用
    T &operator*() const { return *ptr_; };

    // ->
    T *operator->() const { return ptr_; }

    // 参与逻辑运算
    operator bool() const { return ptr_; }


private:
    T *ptr_{nullptr};
};


int main() {
    Shape *s = new Shape();
    // 自定义构造函数
    SmartPtr<Shape> sp{s};

    SmartPtr<Shape> sp1;
    sp1 = std::move(sp);

//    SmartPtr<Shape> sp1{std::move(sp)};

    return 0;
}

