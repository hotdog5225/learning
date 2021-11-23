# 函数和类也是对象object，属于python的一等公民
# 	1. 赋值给一个变量
# 	2. 可以添加到集合对象中
# 	3. 可以作为参数传递给函数
# 	4. 可以当做函数的返回值

# 	1. 赋值给一个变量
def func():
    print("hello")


my_func = func
my_func()


class Person:
    def __init__(self):
        print("person")


my_class = Person
my_class()

# 	2. 可以添加到集合对象中
my_list = []
my_list.append(my_func)
my_list.append(my_class)
for item in my_list:
    item()


# 	3. 可以作为参数传递给函数
def func2(Person):
    p = Person()


# 	4. 可以当做函数的返回值
def my_decorate_func():
    return my_func


decorate_func = my_decorate_func()
decorate_func()
