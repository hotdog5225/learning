# memory address
a = 1
print(id(a))  # 4448594272

# None 对象, 全局唯一
a = None
b = None
print(id(a) == id(b))  # True

# python中的常见内置类型
# 	对象的三个特征
# 		身份
# 		类型
# 		值
# 	None(全局只有一个)
# 	数值
# 		int
# 		float
# 		complex（复数）
# 		bool
# 	迭代类型
# 	序列类型
# 		list
# 		bytes、bytearray、memoryview（二进制序列）
# 		range
# 		tuple
# 		str
# 		array
# 	映射(dict)
# 	集合
# 		set
# 		frozenset
# 	上下文管理类型（with）
# 	其他
# 		模块类型
# 		class和实例
# 		函数类型
# 		方法类型
# 		代码类型
# 		object对象
# 		type类型
# 		ellipsis类型
# 		notimplemented类型
