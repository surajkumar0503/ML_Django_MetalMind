# fp = open('C:\Users\Python2\Desktop\doc\mod\text1.txt', 'x')
# fp.close()
#

# fp = open('sales.txt', 'w')
# fp.writelines('second line')
# fp.close()
#

# fp = open('sales.txt', "r")
# print(fp.readlines())
# fp.close()

# import os

# # Absolute path of a file
# old_name = "sales.txt"
# new_name = "new.txt"
#
# # Renaming the file
# os.rename(old_name, new_name)
# os.remove('sales_1')

# fp = open('new.txt', 'a')
# fp.write('123')
# fp.close()

# class operations:
#     def add(self):
#         a, b = 4, 2
#         c = a+b
#         print(c)
#
#     def sub(self):
#         a, b = 4, 3
#         c= a-b
#         print(c)
#
#
# obj = operations()
# obj.add()
# obj.sub()

class Cat:
    # def __init__(self, name, age):
    #     self.name = name
    #     self.age = age

    def info(self):
        print(f"I am a cat. My name is . I am  years old.")

    def make_sound(self):
        print("Meow")

# cat1 = Cat('Andy', 2)
# cat2 = Cat('Phoebe', 3)
cat1 = Cat()
cat2 = Cat()
cat2.info()