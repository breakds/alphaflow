from functools import wraps


def make_node(init):
    import inspect
    arg_names = inspect.getargspec(init)[0]

    @wraps(init)
    def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        for arg_name, arg_value in zip(arg_names[1:], args):
            # Special handling for list for one level
            if type(arg_value) is list:
                for element in arg_value:
                    self._try_add_dep(element)
            else:
                self._try_add_dep(arg_value)
            
        node_name = self.__class__.__name__
        
        for arg_name, arg_value in kwargs.items():
            if arg_name == 'name':
                node_name = arg_value
        self._set_name(node_name)

    return new_init


class Node(object):
    """Base class for all node in the computation graph.

    Nodes are allowed to refer to the other nodes, allowing to nest
    them in a tree (more strictly DAG) structure.

    """

    def __init__(self):
        # TODO(breakds): Use a enum to represent different status such
        # as RUNNING and REALIZED.
        self.name = 'NONAME'
        self.realized = False
        self.cached_result = None
        self.dependencies = []


    def _set_name(self, name):
          self.name = name
    

    def _try_add_dep(self, dep):
        """Add a dependency if it is also a Node.
        """
        if issubclass(type(dep), Node):
            self.dependencies.append(dep)

    def evaluate(self):
        pass

    def value(self):
        if not self.realized:
            self.cached_result = self.evaluate()
            self.realized = True
        return self.cached_result
