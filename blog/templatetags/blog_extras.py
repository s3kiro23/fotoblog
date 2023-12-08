from django import template
from django.utils.timezone import now

register = template.Library()

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username


@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'Posté il y a {int(seconds_ago // MINUTE)} minutes'
    elif seconds_ago <= DAY:
        return f'Posté il y a {int(seconds_ago // HOUR)} heures'
    return f'Posté le {posted_at.strftime("%d %b %y à %Hh%M")}'
