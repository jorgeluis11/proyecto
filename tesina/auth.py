from profiles.models import NotasoUser


class CustomAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = NotasoUser.objects.get(email=username)
            return user
        except:
            return

    def get_user(self, user_id):
        try:
            user = NotasoUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except UserProfile.DoesNotExist:
            return None
