

from datetime import timedelta

from django.utils import timezone

from users.models import Progress, Tasks, Users


def get_avarege_progress():
    done_tasks = Tasks.objects.filter(status = True)
    all_tsk = Tasks.objects.all()
    if all_tsk.count() == 0:
        return 0
    avarege_progress = (done_tasks.count() / all_tsk.count()) * 100

    return round(avarege_progress)

def get_activity_percentage():
    period_start = timezone.now() - timedelta(days=7)
    total_users = Users.objects.count()
    
    if total_users == 0:
        return 0
    
    active_users = Progress.objects.filter(
        created_at__gte=period_start
    ).values('user').distinct().count()
    
    return int((active_users / total_users) * 100)
