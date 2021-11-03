import re

# . 除了 换行符号\n 之外的 匹配
one = """
    msfdsdffdsdfsn
    1234567778888N
"""

# re.S : dot可以匹配换行符
# re.I : 忽略大小写
pattern = re.compile('m(.*)n', re.S | re.I)
result = pattern.findall(one)
print(result)
