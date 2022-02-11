//
// Created by wuzewei.wzw on 2021/11/15.
//

#include "TestClass.h"
#include "IntArray.h"

int main() {
    // unsigned signed类型转换

    // 1. 给无符号类型的变量, 赋一个超过表示范围的值, 得到的结果是取模后的值.
    unsigned char char_a = -1; // 将负数 -1 转成 无符号数
    // 取模计算过程
    //      取模: -1 / 256 向 -∞ 取整 ==> 得到-1
    //      获取余数: -1 - (-1) * 256 = 255
    std::cout << "[负数 -1 转成无符号数 unsigned char]: " << int(char_a) << std::endl;
    // 也可以这么理解:
    // 如果将负数, 转成unsigned值. 则相当于负数直接加上模. 即: -1 + 256 ==> 255

    // 2. unsigned和signed出现在同一个表达式中, unsigned会先转成unsigned进行计算
    unsigned char un_char_a2 = 10;
    char char_b2 = -1;
    std::cout << "[有符号数 -1 会先转成无符号数 unsigned char, 再计算]: " << (un_char_a2 + char_b2) << std::endl;
    // 计算过程
    //      char_b2转为unsigned: -1 ==> 255
    //      char_b2 + un_char_a2: 255 + 10 ==> 265 ==> 超过了unsigned char表示范围 ==> 取模: 265 - 1*255 = 9

    // 3. 给有符号数, 赋值超过表示范围的值, 得到的是undefined的值
//    char a = 256;
//    std::cout << "undefined:" << int(a) << std::endl;

    std::cout << "\n";
    /*------------------*/

    // 列表初始化 list initialization
    int int_a{5};
//    int int_b{5.0}; // 初始值精度丢失, 无法使用list initialization初始化

    // 虽然OK, 但会精度丢失
    int int_c(5.0);
    int int_d = 5.0;

    /*------------------*/

    // call default constructor
    TestClass non_const_t1{}; // list initialization(with empty brace): will do "value initialization, init member to zero". better than TestClass non_const_t1(default initialization);

    // call according constructor
    TestClass non_const_t2{"hotdog5225"}; // list initialization : call according constructor

    // call according Constructor, and initiate const member with "member initializer list".
    TestClass non_const_t3{"hotdog", "hotdog_const"};

    /*------------------*/

    // initialize static member vector<int>
    // call static member directly by Class
    std::cout << "[call static member through Class]: ";
    for (const auto int_member: TestClass::static_vec) {
        std::cout << std::to_string(int_member) << ", ";
    }
    std::cout << '\n';

    /*------------------*/

    // static function called, use Class Name as prefix
    std::cout << TestClass::get_private_static_member() << std::endl;

    /*------------------*/

    // use list initialization to initialize IntArray(customized object)
    IntArray ia{1, 2, 3, 4, 5};
//    ia.printArray();

    // use  list assignment to initialize IntArray(customized object)
    IntArray ia2 = {10, 9, 8, 7};
//    ia2.printArray();

    return 0;
}