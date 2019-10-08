from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Sum

from companies.models import Company, Job

ROLES = (
    (1, "job_seeker"),
    (2, "employee"),
)


class User(AbstractBaseUser, PermissionsMixin):
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
    full_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    job_seeker_intro = models.TextField(blank=True)
    employee_intro = models.TextField(blank=True)
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

    def balance(self):
        """
        Calculate balance from purchase history
        :return: point balance
        """
        return (self.incomings.aggregate(Sum('amount'))['amount__sum'] or 0) - \
               (self.outgoings.aggregate(Sum('amount'))['amount__sum'] or 0)

    def __str__(self):
        return f'User {self.email}'

    class Meta:
        db_table = "users"
