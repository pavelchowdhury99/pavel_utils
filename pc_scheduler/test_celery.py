from fastapi import FastAPI
from pc_scheduler.celery_app import app, test_function, AsyncResult
# from celery.task.control import revoke
from time import sleep

my_app = FastAPI()


@my_app.get("/test/{num}")
def test(num):
    res1 = test_function.delay(int(num))
    return {'id': res1.task_id, 'status': res1.status}


@my_app.get("/get_test/{task_id}")
def test(task_id):
    res1 = AsyncResult(task_id)
    return {'result': res1.get()}


@my_app.get("/get_staus/{task_id}")
def test(task_id):
    res1 = AsyncResult(task_id,app=app)
    return {'status': res1.status}

# print(test_function(5))