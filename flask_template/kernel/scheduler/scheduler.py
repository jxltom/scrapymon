from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import arrow


class Scheduler:

    def __init__(self):
        """Init scheduler and store results."""
        self._scheduler = BackgroundScheduler()
        self._results = {}
        self._scheduler.add_listener(self._update_result,
                                     EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def _update_result(self, event):
        """Update result when the job is finished."""
        self._results[event.job_id].append(event.retval)

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown()

    def add_daily_job(self, job_id, func, time):
        """Add job at specific time everyday."""
        hour, minute = map(int, time.split(':'))
        self._scheduler.add_job(id=job_id, func=func,
                                trigger='cron',
                                hour=hour, minute=minute,
                                timezone='Asia/Hong_Kong')
        self._results[job_id] = []

    def add_interval_job(self, job_id, func, **interval):
        """
        Add job which will run at interval.
        The keyword argument can be hours, minutes, seconds.
        """
        self._scheduler.add_job(id=job_id, func=func,
                                trigger='interval', **interval)
        self._results[job_id] = []

    def remove_job(self, job_id):
        self._scheduler.remove_job(job_id)

    def check_job_all_results(self, job_id):
        return self._results[job_id]

    def check_job_latest_result(self):
        pass

    def print_jobs(self):
        return self._scheduler.print_jobs()
