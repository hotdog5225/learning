//
// Display::PrintStoragePrivateMember is a friendly member function to Class Storage
//

#include "Storage.h" // to satisfy (1)

// when compile comes to here, it already knows the all member definition of Class Storage. so member can be accessed in the function
void Display::PrintStoragePrivateMember(const Storage &storage) {
    std::cout << storage.m_name << std::endl; // (1) compile need to know all definition of Class Storage ( what members it has)
}