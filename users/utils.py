from datetime import timedelta
import re

from django.db.models import (
    F,
    Q,
    Case,
    Count,
    ExpressionWrapper,
    FloatField,
    IntegerField,
    Max,
    Value,
    When,
)

from django.utils import timezone
from users.models import Progress, Tasks, Users
from django.db.models.functions import Cast


def q_search(query):
    return Users.objects.filter(
        Q(username__icontains=query)
        | Q(email__icontains=query)
        | Q(role__icontains=query)
    )

def get_users_with_stats():
    all_users = Users.objects.annotate(
        total_tasks=Count("progress"),  # Все задачи пользователя
        completed_tasks=Count("progress", filter=Q(progress__task__status=True)),
        progress_percent=Case(
            When(total_tasks=0, then=Value(0)),
            default=ExpressionWrapper(
                Cast(F("completed_tasks"), FloatField())
                / Cast(F("total_tasks"), FloatField())
                * 100,
                output_field=IntegerField(),
            ),
        ),
    )
    return all_users

def get_max_progress(queryset = None):
    if queryset is None:
        queryset = get_users_with_stats()
    return queryset.aggregate(max_progress=Max("progress_percent"))["max_progress"] or 0


def get_leader_name():
    all_users = get_users_with_stats()
    max_progress = get_max_progress(all_users)
    return all_users.filter(progress_percent=max_progress).first().username



def get_activity_for_user(user):
    period_start = timezone.now() - timedelta(days=30)
    total_tasks = Progress.objects.filter(user=user).count()
    issues_created_in_last_month = Progress.objects.filter(
        user=user, created_at__gte=period_start
    ).count()

    if total_tasks == 0:
        return 0

    # done_tasks = Progress.objects.filter(
    #     user = user,
    #     created_at__gte = period_start,
    #     task__status = True
    # ).count()

    return int((issues_created_in_last_month / 10) * 100)


def new_users_last_week():
    period_start = timezone.now() - timedelta(days=7)
    if Users.objects.filter(date_joined__gte=period_start).count() == 0:
        return 0
    return Users.objects.filter(date_joined__gte=period_start).count()





def count_leaders():
    all_users = get_users_with_stats()
    if all_users:
        max_progress = max([user.progress_percent for user in all_users], default=0)
        counter = 0
        for user in all_users:
            if user.progress_percent == max_progress:
                counter += 1
    return counter


