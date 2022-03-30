from functools import partial  # карирование
from django.contrib.auth.decorators import user_passes_test

# superuser_required = user_passes_test(lambda u: u.is_superuser)
# superuser_required = partial(user_passes_test(lambda u: u.is_superuser))
def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)
