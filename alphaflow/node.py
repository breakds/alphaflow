from functools import wraps
import concurrent.futures

from graphviz import Digraph

from .scheduler import Scheduler


def make_node(init):
    """The decorator for __init__ of all the Node derived class.

    This decorator mainly serves two purposes.

    1) Pick up the meaning ful keyword argument such as `name`

    2) Detect the inputs whose class is derived from Node and add them
       to the dependency list automatically

    """
    import inspect
    arg_names = inspect.getargspec(init)[0]

    @wraps(init)
    def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        for arg_value in args:
            # Special handling for list for one level
            if type(arg_value) is list:
                for element in arg_value:
                    self._try_add_dep(element)
            else:
                self._try_add_dep(arg_value)

        # The name of the node will be set to its class name if not specified.
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
        # Default value for the name. This will be override as soon as
        # the @make_node decorator is applied.
        self.name = 'NONAME'

        # Will be set to True once the node is evaluated.
        self.realized = False

        # Will hold the final result of the evaluation after the node
        # is evaluated.
        self.cached_result = None

        # This will be automatically populated by @make_node decorator
        # to memorize all the dependencies of this node
        self.dependencies = []


    def _set_name(self, name):
        """Set the name of the node."""
        self.name = name
    

    def _try_add_dep(self, dep):
        """Add a dependency if it is also a Node.
        """
        if issubclass(type(dep), Node):
            self.dependencies.append(dep)


    def evaluate(self):
        """Override this to implement the actual node logic."""
        pass


    def _ensure_evalauted(self):
        """Internal helper function evluate this node if it is not yet.

        The evaluation make uses of the (global) Scheduler.
        """
        if self.realized:
            return

        running = []
        for dep in self.dependencies:
            if not dep.realized:
                running.append(Scheduler().submit(dep._ensure_evalauted, dep))
        concurrent.futures.wait(running)
        self.cached_result = self.evaluate()
        self.realized = True


    def value(self):
        """Access the evaluated result.

        If the node is not evaluated yet, calling value() will force it to be
        evalauted.

        """
        self._ensure_evalauted()
        return self.cached_result


    def get_dag(self):
        """Access the DAG that visualize the dependencies."""
        dot = Digraph(format = 'png')
        stack = [self]
        all_nodes = set()
        while len(stack) > 0:
            current = stack.pop()
            if current in all_nodes:
                continue
            all_nodes.add(current)
            for dep in current.dependencies:
                dot.edge(f'n{id(dep)}', f'n{id(current)}')
                if dep not in all_nodes:
                    stack.append(dep)

        for node in all_nodes:
            dot.node(f'n{id(node)}', node.name)

        return dot
            
            
