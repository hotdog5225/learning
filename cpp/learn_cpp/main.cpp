#include <iostream>

template<typename T>
// template type declaration
T sya_hello(T a) {
    std::cout << "[template function] called: " << a << '\n' << std::endl;
    return a;
}

// used for std::bind
void test_func(int a) {
    std::cout << "[std::bind] : " << a << '\n' << std::endl;
}

int main() {
    // template function called
    sya_hello(3);

    /*------------------*/

    // std::bind
    auto f = std::bind(test_func, std::placeholders::_1);
    f(1);

    return 0;
}