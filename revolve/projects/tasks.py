from celery import shared_task


@shared_task
def testing():
    print("Testing celery")
