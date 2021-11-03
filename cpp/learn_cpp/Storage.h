//
// Class Storage has a friendly member function : Display::PrintStoragePrivateMember
//

#ifndef LEARN_CPP_STORAGE_H
#define LEARN_CPP_STORAGE_H

#include <iostream>
#include "Display.h" // to satisfy (1)

class Storage {
private:
    std::string name{};

// friend member function declaration (can be declared either in private: or public:)
friend void Display::PrintStoragePrivateMember(const Storage &storage); // (1) compile need to know specific member function proto of Display::PrintStoragePrivateMember

};


#endif //LEARN_CPP_STORAGE_H
