from django import template
from datetime import datetime
register = template.Library()

@register.filter
def get_greeting(user):
    # Use datetime.now() to get the current time
    current_time = datetime.now()

    if 0 <= current_time.hour < 12:
        return f"Good morning {user.first_name}!"
    elif 12 <= current_time.hour < 18:
        return f"Good afternoon {user.first_name}!"
    elif 18 <= current_time.hour < 20:
        return f"Good evening {user.first_name}!"
    else:
        return f"Good night {user.first_name}!"
