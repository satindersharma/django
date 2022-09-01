from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(get_user_model().USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            # # user = get_user_model()._default_manager.get_by_natural_key(username)
            # user = get_user_model()._default_manager.get(
            #     Q(username__iexact=username) | Q(email__iexact=username))
            
            users = get_user_model()._default_manager.filter(
            Q(username__iexact=username) | Q(email__iexact=username))
            if users:
                for user in users:
                    if user.check_password(password):
                        return user
            else:
                return None
        except get_user_model().DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            get_user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
