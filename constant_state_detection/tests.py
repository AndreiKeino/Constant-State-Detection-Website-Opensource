from django.test import TestCase

# Create your tests here.

class A:

    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'object of the class A: a = {self.a}; b = {self.b}'

class B(A):

    def __init__(self,c, a=None, b=None):
        super().__init__(a, b)
        self.c = c


    def __repr__(self):
        return (f'object of the class B: a = {self.a}; b = {self.b} '
                f' c = {self.c}')

a_obj = A()
print(a_obj)

b_obj = B(8, 16, 24)
print(b_obj)

