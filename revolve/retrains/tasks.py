from celery.schedules import crontab

from celery import shared_task, on_after_configure


@on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@shared_task
def test(arg):
    print(arg)
