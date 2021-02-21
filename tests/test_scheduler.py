import unittest

from alphaflow import Scheduler


def my_task(n):
    sum = 0
    for i in range(n + 1):
        sum += i
    return sum


class SchedulerTest(unittest.TestCase):
    def test_scheduler_singleton(self):
        a = Scheduler()
        b = Scheduler()
        self.assertEqual(a, b)


    def test_set_num_workers(self):
        Scheduler().use_n_cpus(8)
        self.assertEqual(8, Scheduler().workers)


    def test_execute_task(self):
        f = Scheduler().submit(my_task, 100)
        self.assertEqual(5050, f.result())
