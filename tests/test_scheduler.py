import unittest
from flask_template.kernel.scheduler.scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    def job_example(self):
        print('executed')
        return 'This is result'

    def setUp(self):
        self.scheduer = Scheduler()

    def test_scheduler(self):
        self.scheduer.start()
        self.scheduer.add_daily_job(job_id='test_daily',
                                    func=self.job_example, time='12:00')
        self.scheduer.print_jobs()
        self.scheduer.check_job_all_results('test_daily')

        self.scheduer.add_interval_job(job_id='test_interval',
                                       func=self.job_example, seconds=1)
        self.scheduer.print_jobs()
        self.scheduer.check_job_all_results('test_interval')
        import time
        time.sleep(5)
        print(self.scheduer.check_job_all_results('test_interval'))
        self.scheduer.shutdown()
