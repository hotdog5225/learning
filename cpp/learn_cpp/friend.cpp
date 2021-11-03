// show how friend member function be defined in a single file

#if 0

    #include <iostream>

    class Storage; // satisfy (1)

    class Display {
    public:
        /*
        void PrintStoragePrivateMember(const Storage& Storage) { // (1) need a Class Storage declaration: compile needs to know the exists of Class Storage
            std::cout << Storage.name << std::endl; // (2)need to know all definition of Class Storage: compile needs to know the exists of member "name"
        }
        */
        void PrintStoragePrivateMember(const Storage& Storage);
    };

    class Storage {
    private:
        std::string name{"hotdog"};

    // friend member function declaration (can be declared either in private: or public:)
    friend void Display::PrintStoragePrivateMember(const Storage &Storage);

    };

    // when compile comes to here, it already knows the all definition of Class Storage. so member can be accessed in the function
    void Display::PrintStoragePrivateMember(const Storage &Storage) {
        std::cout << Storage.name << std::endl;
    }

#endif