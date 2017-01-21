from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import (EVENT_JOB_EXECUTED, EVENT_JOB_ERROR,
                                EVENT_JOB_ADDED, EVENT_JOB_REMOVED)
import arrow


class Scheduler:

    def __init__(self):
        """Init scheduler and store results."""
        self._scheduler = BackgroundScheduler(timezone='Asia/Hong_Kong')
        self._result_store, self._status_store = {}, {}
        self._scheduler.add_listener(self._job_execution_event,
                                     EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._scheduler.add_listener(self._job_add_event, EVENT_JOB_ADDED)
        self._scheduler.add_listener(self._job_remove_event, EVENT_JOB_REMOVED)

    def _job_execution_event(self, event):
        """Store job result when the job finishes or error happens."""
        time = arrow.utcnow().to('Asia/Hong_Kong').format()
        result = str(event.exception) if event.exception else event.retval
        self._result_store[event.job_id].append([time, result])

    def _job_add_event(self, event):
        """Set the job status to True and init result store."""
        self._status_store[event.job_id] = True
        if not self._result_store.get(event.job_id):
            self._result_store[event.job_id] = []

    def _job_remove_event(self, event):
        """Set the job status to False"""
        self._status_store[event.job_id] = False

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown(wait=False)

    def enable_job(self, job, trigger, **kwargs):
        """
        Enable job which will run everyday at specific time or job which will
        run at specific interval. When trigger is daily, keyword argument should
        be time which has format of HH:mm. When trigger is interval, keyword
        arguments can be hours, minutes, or seconds.
        """
        self.disable_job(job)

        if trigger == 'daily':
            time = kwargs.get('time')
            hour, minute = map(int, time.split(':'))
            self._scheduler.add_job(id=job.job_id, func=job.func,
                                    trigger='cron',
                                    hour=hour, minute=minute)
        elif trigger == 'interval':
            self._scheduler.add_job(id=job.job_id, func=job.func,
                                    trigger='interval', **kwargs)
        else:
            raise Exception('No job type is matched')

    def disable_job(self, job):
        """Disable a job."""
        if self._status_store.get(job.job_id):
            self._scheduler.remove_job(job.job_id)

    def get_result(self, job, latest=True):
        """Return results of a job."""
        results = self._result_store.get(job.job_id, [])
        return results if not latest else results[0] if results else []

    def get_status(self, job):
        """Return status of a job."""
        if self._status_store.get(job.job_id) is None:
            return False
        else:
            return self._status_store[job.job_id]

    def print_jobs(self):
        self._scheduler.print_jobs()
