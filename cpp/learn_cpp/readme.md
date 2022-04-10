# const

- const member
- const member function
- const class object

# initialization

- signed(负数) 转成 unsigned: 取模运算(可以直接简记为: 负数+模)
- constructor
    - default constructor
    - custom constructor
- destructor
- list initialization: `{}`
    - static member
    - static function
- std::initializer_list for customer object
- member initializer list `:member{value}`
- static
- non_static_member_initialization.cpp
    - 给non-static class member 提供 初始化默认值

# reference_and_pointer

- const reference
- pointer to const variable `const *`
- const pointer: `* const`
- const member function return const reference

# friend

- friend member function in a single file
- friend member function in separate file

# object relation

- std::reference_wrapper

# inheritance

- construct call order
- initialize member of Base, when constructor of Derived class called

# static
- 定义,初始化 static-member-variable
- 通过static_member_func直接访问static_member_variable