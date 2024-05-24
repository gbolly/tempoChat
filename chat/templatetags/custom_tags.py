from django import template
from django.utils.timezone import now

register = template.Library()


@register.filter
def minutes_since_last_login(user):
    if user.last_login:
        time_since_last_login = now() - user.last_login
        return int(time_since_last_login.total_seconds() / 60)
    return None
