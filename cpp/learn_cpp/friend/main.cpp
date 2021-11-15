//
// Created by wuzewei.wzw on 2021/11/15.
//

#include "Storage.h"

int main() {
    Storage s{"hotdog"};
    Display d;
    d.PrintStoragePrivateMember(s);
    return 0;
}