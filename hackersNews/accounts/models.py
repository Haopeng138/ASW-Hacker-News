from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from api.models import UserAPIKey

# Create your models here.

# User Manager
class HackerNewsUserManager(BaseUserManager):

    def create_empty_user(self):
        user = self.model(date_joined=datetime.date.today())
        user.database = self._db
        return user

    def create_user(self, username, email, password=None):
        # Crea y guarda un usuario
        print ("Se ha usado HackerNewsUserManager")

        if not email:
            raise ValueError('Email field cannot be empty')

        user = self.create_empty_user()

        user.email = email
        user.username = username
        user.set_password(password)

        user.save(using=self._db)
        api_key, key = UserAPIKey.objects.create_key(name=user.username, user=user)
        print(api_key)
        print(key)
        user.key = key
        user.save(using=self._db)
        UserAPIKey.objects.create_key(user=user)

        return user

    # Crea un usuario admin
    def create_superuser(self, email, username, password=None):
        user = self.create_user(username, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Model de Usuario
class HNUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    karma = models.IntegerField(default=0)

    key = models.CharField()

    date_joined = models.DateField(auto_now_add=True)
    about = models.TextField(default='')

    # Necesario para crear admins
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Especifica que identidfica un usuario
    EMAIL_FIELD = 'email'  # Accesible mediante get_email_field_name()
    REQUIRED_FIELDS = ['username']  # password y USERNAME_FIELD simpre son requeridos
    # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    objects = HackerNewsUserManager()

    def __str__(self):
        return self.username

    def get_username(self):
        return super().get_username()

    # Quizas util?
    def get_absolute_url(self):
        return "/users/%i/" % self.id

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
