# AlphaFlow

The minimalist's toolkit for building DAG-based pipelines.

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
a = Factorial(5, name = 'F5!')
b = Factorial(6, name = 'F6!')
c = Factorial(6, name = 'F7!')
d = Factorial(6, name = 'F8!')
result = create_recursive_sum(a, b, c, d)
```

Visualize the computation graph.

```python
result.get_dag()
```

![generated dag](/images/Digraph.gv.pdf)

## How to run the unit tests

```
python -m unittest
```

will run all the tests with automatical [Test Discovery](https://docs.python.org/3/library/unittest.html#unittest-test-discovery).

To run a specific test file

```
python -m unittest path/to/that/test/file.py
```
