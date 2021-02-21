# alphaflow
A minimalist's computation graph based pipeline system in python

## Example

Defining the computation graph nodes and functions as building blocks.

```python
from alphaflow import Node, make_node
import math

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
    
    
def create_recursive_sum(*args):
    if len(args) == 0:
        return Constant(0)
    
    func = args[0]
    for arg in args[1:]:
        func = Add(arg, func)

    return func
```

Actually make use of the nodes to build computational graph.

```python
a = Factorial(1, name = 'F1!')
b = Factorial(2, name = 'F2!')
c = Factorial(3, name = 'F3!')
d = Factorial(4, name = 'F4!')
result = create_recursive_sum(a, b, c, d)
```

Visualize the computation graph.

```python
result.get_dag()
```

![generated dag](/images/sum.png)


