from django.db.models import Q

from users.models import Users


def q_search(query):
    return Users.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(role__icontains=query)
    )
