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

// public inheritance:
// - public     -> public (can be accessed by anybody)
// - protected  -> protected
// - private    -> inaccessible
class Pub: public Base {
};

// protected inheritance:
// - public     -> protected (only can be accessed by Member, Friend and Derived)
// - protected  -> protected
// - private    -> inaccessible
class Pro: protected Base {
};

// protected private:
// - public     -> private (can only be accessed by Member, Friend)
// - protected  -> private
// - private    -> inaccessible
class Pri: private Base{};