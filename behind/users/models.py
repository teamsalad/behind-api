from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from companies.models import Company, Job


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        (1, "job_seeker"),
        (2, "employee"),
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=20,
        unique=True,
        help_text='Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=ROLES[0][0]
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text=
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"


class UserJobHistory(models.Model):
    METHODS = (
        (1, "email"),
        (2, "business_card"),
        (3, "proof_of_employment"),
    )
    confirmation_method = models.PositiveSmallIntegerField(
        choices=METHODS,
        default=METHODS[0][0]
    )
    confirmed = models.BooleanField(default=False)
    confirmation_information = models.TextField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    company = models.OneToOneField(
        Company,
        on_delete=models.SET_NULL,
        null=True
    )
    job = models.OneToOneField(
        Job,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_job_histories"
