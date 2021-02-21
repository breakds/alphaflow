import concurrent.futures
import multiprocessing


class Scheduler(object):
    """The Scheduler is used to execute node evaluation asynchronously.

    Under the hood it is a singleton that wraps a thread pool
    executor.

    """

    _instance = None

    def __new__(cls):
        """Override __new__ to implement the singleton pattern.

        This means that when never Scheduler() is called, it always
        returns exactly the same instance.

        """

        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.workers = 4
            cls._instance.executor = concurrent.futures.ThreadPoolExecutor(max_workers = 4)
        return cls._instance


    def use_n_cpus(self, n):
        """Set the number of workers to n."""
        self.workers = n
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers = n)
    

    def use_max_cpus(self):
        """Set the number of workers to be the number of cpus on this machine."""
        self.use_n_cpus(multiprocessing.cpu_count())


    def use_half_cpus(self):
        """Set the number of workers to be the half of cpus on this machine."""
        cpu_count = max(int(multiprocessing.cpu_count() / 2), 1)
        self.use_half_cpus(cpu_count)


    def submit(self, *args, **kargs):
        """Main API to submit a task."""
        return self.executor.submit(*args, **kargs)
