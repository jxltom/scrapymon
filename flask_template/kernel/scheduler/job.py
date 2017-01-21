class Job:

    def __init__(self, job_id, func):
        self._job_id = job_id
        self._func = func

    @property
    def job_id(self):
        return self._job_id

    @property
    def func(self):
        return self._func
