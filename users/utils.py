from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from users.models import Progress, Tasks, Users


def q_search(query):
    return Users.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(role__icontains=query)
    )


def get_activity_for_user(user):
    period_start = timezone.now() - timedelta(days=30)
    total_tasks = Progress.objects.filter(user=user).count()
    issues_created_in_last_month =Progress.objects.filter(
        user = user,
        created_at__gte = period_start
    ).count()
    
    if total_tasks == 0:
        return 0
    
    # done_tasks = Progress.objects.filter(
    #     user = user,
    #     created_at__gte = period_start,
    #     task__status = True
    # ).count()
    
    return int((issues_created_in_last_month / 10) * 100)