from functools import wraps
import concurrent.futures

from graphviz import Digraph

from .scheduler import Scheduler


def make_node(init):
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


    def _ensure_evalauted(self):
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
        self._ensure_evalauted()
        return self.cached_result


    def get_dag(self):
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
            
            
