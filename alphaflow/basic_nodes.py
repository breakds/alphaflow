from .node import make_node, Node

class Constant(Node):
    @make_node
    def __init__(self, value, **kargs):
        super().__init__()
        self.realized = True
        self.cached_result = value
