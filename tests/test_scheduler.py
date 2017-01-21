import unittest
import time
from flask_template.kernel.scheduler.scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    @staticmethod
    def _job_normal():
        return 'This is result'

    @staticmethod
    def _job_exception():
        0/0
        return 'This is result'

    def setUp(self):
        self.scheduer = Scheduler()
        self.scheduer.start()

    def test_disable_job_and_get_status(self):
        # test when job doesn't exist
        self.scheduer.disable_job('job_normal')
        self.assertFalse(self.scheduer.get_status('job_normal'))

        # test when job exists
        self.scheduer.enable_job('job_normal', self._job_normal,
                                 trigger='daily', time='00:01')
        self.assertTrue(self.scheduer.get_status('job_normal'))

        # test disable_job
        self.scheduer.disable_job('job_normal')
        self.assertFalse(self.scheduer.get_status('job_normal'))

    def test_get_result(self):
        # test when job doesn't exist
        self.assertEqual(
            self.scheduer.get_result('job_normal', latest=True), [])
        self.assertEqual(
            self.scheduer.get_result('job_normal', latest=False), [])

        # test when job exists
        self.scheduer.enable_job('job_normal', self._job_normal,
                                 trigger='interval', seconds=1)
        time.sleep(3)
        self.assertEqual(
            self.scheduer.get_result('job_normal')[1], 'This is result')
        self.assertTrue(
            type(self.scheduer.get_result('job_normal', latest=False)), list)
        self.assertTrue(
            type(self.scheduer.get_result('job_normal', latest=False)[0]), list)
        self.assertTrue(
            len(self.scheduer.get_result('job_normal', latest=False)) > 1)

    def test_enable_job(self):
        # test daily job
        self.scheduer.enable_job(
            'job_normal', self._job_normal, trigger='daily', time='12:00')
        self.scheduer.print_jobs()

        # test interval job
        self.scheduer.enable_job('job_normal', self._job_normal,
                                 trigger='interval', seconds=1)
        self.scheduer.print_jobs()
        time.sleep(3)
        self.assertTrue(
            len(self.scheduer.get_result('job_normal', latest=False)) > 1)
        self.assertTrue(type(self.scheduer.get_result('job_normal')[0]), str)

        # test enable multiple times
        self.scheduer.enable_job('job_normal', self._job_normal,
                                 trigger='interval', seconds=1)
        time.sleep(2)
        self.scheduer.enable_job('job_normal', self._job_normal,
                                 trigger='interval', seconds=1)
        self.assertTrue(
            len(self.scheduer.get_result('job_normal', latest=False)) > 1)

    def test_exception_in_job(self):
        self.scheduer.enable_job(
            'job_exception', self._job_exception, trigger='interval', seconds=1)
        time.sleep(3)
        self.assertTrue('division by zero'
                        in self.scheduer.get_result('job_exception')[1])

    def tearDown(self):
        self.scheduer.shutdown()
