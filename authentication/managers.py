from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import re

class CustomUserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):

        if not email: #where to put the email validation in managers or the custom user 
            raise ValueError(_("The Email must be set"))
        
        email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_regex, email):
            raise ValueError("Invalid Email format")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        pass
        # extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_active", True)

        # if extra_fields.get("is_staff") is not True:
        #     raise ValueError(_("Superuser must have is_staff=True."))
        # if extra_fields.get("is_superuser") is not True:
        #     raise ValueError(_("Superuser must have is_superuser=True."))
        # return self.create_user(email, password, **extra_fields)