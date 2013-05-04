from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from jsonfield import JSONField

# >>> from django.contrib.auth import get_user_model
# >>> get_user_model()


class NotasoUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            msg = 'Users must have an email address'
            raise ValueError(msg)

        user = self.model(
            email=NotasoUserManager.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class NotasoUser(AbstractBaseUser, PermissionsMixin):
    """ Inherits from both the AbstractBaseUser and
        PermissionMixin.
    """
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=160,
        unique=True,
        db_index=True,
    )
    facebook_id = models.BigIntegerField(blank=True, unique=True, null=True)
    facebook_name = models.CharField(max_length=80, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    raw_data = JSONField(blank=True, null=True)
    notaso_user_id = models.CharField(max_length=11, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = NotasoUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name