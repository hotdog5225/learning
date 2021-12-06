//
// Created by 吴泽伟 on 2021/12/7.
//

class Base {
// can only be accessed by Base member, Friend
private:
    int m_private{};

// can be accessed by Base member, Friend, Derived
protected:
    int m_protected{};

// can be accessed by anybody
public:
    int m_public{};
};

class Derived: public Base {
};