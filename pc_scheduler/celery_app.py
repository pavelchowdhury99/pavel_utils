from celery.result import AsyncResult
from celery import Celery
from time import sleep

app = Celery('tasks', backend='redis://localhost:6379', broker='redis://localhost:6379')

app.conf.update(
    task_track_started=True,
    CELERY_TRACK_STARTED=True
)


@app.task
def test_function(num):
    print('sleping for 5 secs')
    sleep(10)
    print('done sleping for 5 secs')
    return (num ** 4)
