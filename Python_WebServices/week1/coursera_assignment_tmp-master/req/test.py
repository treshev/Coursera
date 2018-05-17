import re

# a1 = '12.12.2000'
# a2 = '1.1'
# a3 = '1'
#
# print(re.match("[0-9]+.[0-9]+.[0-9]+", a1))
# print(re.match("[0-9].[0-9].[0-9]", a2))
# print(re.match("[0-9].[0-9].[0-9]", a3))

text = "a123b45с6d"
exp = r'(\d+)'  # Тут напишите своё регулярное выражение
print(re.findall(exp, text))
