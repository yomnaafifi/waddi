from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if (
            not email
        ):  # where to put the email validation in managers or the custom user
            raise ValueError(_("The Email must be set"))

        email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_regex, email):
            raise ValueError("Invalid Email format")

        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    def validate_phone_number(value):
        pattern = r"^01[0-2]\d{1}-?\d{3}-?\d{4}$"
        if not re.match(pattern, value):
            raise ValidationError(_("Phone number isn't correct"))

    email_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        message="Enter a valid email address.",
    )
    email = models.EmailField(unique=True, validators=[email_validator])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    image = models.ImageField(upload_to=None)  # further edits needed
    phone_no = models.CharField(max_length=100, validators=[validate_phone_number])

    @property
    def age(self):
        today = date.today()
        age = (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

        if age < 18:
            raise ValidationError("You must be 18 or older to sign up.")
        return age

    is_customer = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "birthdate", "phone_no"]

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
