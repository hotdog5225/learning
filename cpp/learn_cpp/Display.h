//
// Display::PrintStoragePrivateMember is a friendly member function to Class Storage
//
#ifndef LEARN_CPP_DISPLAY_H
#define LEARN_CPP_DISPLAY_H

class Storage; // forward declaration: to satisfy (1), NOTE: no need for #include "Storage.h" (when need to know all definition of Storage Class"

class Display {
public:
    void PrintStoragePrivateMember(const Storage& s); // (1) need a Class Storage declaration: compile needs to know the exists of Class Storage
};


#endif //LEARN_CPP_DISPLAY_H
