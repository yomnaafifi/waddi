from django.contrib.auth.models import AbstractBaseUser
from authentication.managers import  CustomUserManager
from django.db import models
from datetime import date 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class CustomUser(AbstractBaseUser):
    def validate_phone_number(value):
        pattern = r'^01[0-2]\d{1}-?\d{3}-?\d{4}$'
        if not re.match(pattern, value):
            raise ValidationError(_("Phone number isn't correct"))

    email = models.EmailField(unique = True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    image = models.ImageField(upload_to=None) # further edits needed 
    phone_no = models.CharField(max_length=100, validators=[validate_phone_number])

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return age

    is_customer = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate', 'phone_no']

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'