from copy import copy

class A:

    def __init__(self, a, b):
        self.a1 = a
        self.a2 = b


class B:

    def __init__(self, a, b):
        self.a = A(a, b)


    def __repr__(self):
        return f'{self.a.a1} {self.a.a2}'

b1 = B(1, 2)
b12 = copy(b1)
b13 = b1

b1 = B(3, 4)

print(b1)
print(b12)
print(b13)
