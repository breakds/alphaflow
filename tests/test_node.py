import unittest
import math

from alphaflow import Node, make_node, Constant


class Factorial(Node):
    @make_node
    def __init__(self, n, **kwargs):
        super().__init__()
        self.n = n


    def evaluate(self):
        return math.factorial(self.n)


class Add(Node):
    @make_node
    def __init__(self, a, b, **kwargs):
        super().__init__()
        self.a = a
        self.b = b


    def evaluate(self):
        return self.a.value() + self.b.value()


class Sum(Node):
    @make_node
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args


    def evaluate(self):
        sum = 0
        for arg in self.args:
            sum += arg.value()
        return sum


def create_recursive_sum(*args):
    if len(args) == 0:
        return Constant(0)
    
    func = args[0]
    for arg in args[1:]:
        func = Add(arg, func)

    return func
    

class TestNode(unittest.TestCase):
    def test_implicit_node_name(self):
        a = Factorial(5)
        self.assertEqual('Factorial', a.name)
        self.assertEqual(120, a.value())


    def test_explicit_node_name(self):
        a = Factorial(6, name = 'F6')
        self.assertEqual('F6', a.name)
        self.assertEqual(720, a.value())


    def test_composition_add_two(self):
        a = Factorial(5, name = 'F5!')
        b = Factorial(6, name = 'F6!')
        c = Add(a, b)
        self.assertEqual(840, c.value())


    def test_sum_four(self):
        a = Factorial(1, name = 'F1!')
        b = Factorial(2, name = 'F2!')
        c = Factorial(3, name = 'F3!')
        d = Factorial(4, name = 'F4!')
        result = Sum(a, b, c, d)
        self.assertEqual(33, result.value())


    def test_add_tree(self):
        a = Factorial(1, name = 'F1!')
        b = Factorial(2, name = 'F2!')
        c = Factorial(3, name = 'F3!')
        d = Factorial(4, name = 'F4!')
        result = Add(Add(a, b), Add(c, d))
        self.assertEqual(33, result.value())


    def test_constant_node(self):
        a = Constant('Great!')
        self.assertEqual('Great!', a.value())


    def test_recursive_sum(self):
        a = Factorial(1, name = 'F1!')
        b = Factorial(2, name = 'F2!')
        c = Factorial(3, name = 'F3!')
        d = Factorial(4, name = 'F4!')
        result = Sum(a, b, c, d)
        self.assertEqual(33, result.value())


if __name__ == '__main__':
    unittest.amin()
