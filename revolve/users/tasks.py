from celery import shared_task
from users.models import User


@shared_task(name="Disabled trial account")
def disabled_trial_account(user_id):
    user = User.objects.get(id=user_id)

    if user:
        if user.account_type == 0:
            user.disabled = True
            user.save(force_update=True)
