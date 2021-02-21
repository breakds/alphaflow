import concurrent.futures
import multiprocessing


class Scheduler(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.workers = 4
            cls._instance.executor = concurrent.futures.ThreadPoolExecutor(max_workers = 4)
        return cls._instance


    def use_n_cpus(self, n):
        self.workers = n
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers = n)
    

    def use_max_cpus(self):
        self.use_n_cpus(multiprocessing.cpu_count())


    def use_half_cpus(self):
        cpu_count = max(int(multiprocessing.cpu_count() / 2), 1)
        self.use_half_cpus(cpu_count)


    def submit(self, *args, **kargs):
        return self.executor.submit(*args, **kargs)
