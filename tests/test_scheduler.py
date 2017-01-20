import unittest
import time
from flask_template.kernel.scheduler.scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    def job_example(self):
        return 'This is result'

    def setUp(self):
        self.scheduer = Scheduler()

    def test_scheduler(self):
        self.scheduer.start()
        self.scheduer.add_daily_job(job_id='test_daily',
                                    func=self.job_example, time='12:00')
        self.scheduer.get_job_all_results('test_daily')

        self.scheduer.add_interval_job(job_id='test_interval',
                                       func=self.job_example, seconds=1)
        self.scheduer.get_job_all_results('test_interval')
        time.sleep(3)
        self.assertTrue(self.scheduer.get_job_all_results('test_interval'))
        self.assertTrue(len(self.scheduer.get_job_all_results('test_interval')))
        self.assertEqual(len(self.scheduer.get_job_latest_result('test_interval')), 1)
        self.scheduer.shutdown()
