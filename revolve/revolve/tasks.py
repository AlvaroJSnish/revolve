from .celery import app


@app.task
def test():
    print('hi from celery')
