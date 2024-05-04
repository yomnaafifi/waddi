from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.models import CustomUser 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re 

PASSWORD_VALIDATION_PATTERN = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_=+{};:,<.>]).{8,}$'

class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password','first_name','last_name','birthdate','phone_no', 'age']


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    


# Password validation regex pattern
    
    def validate_password(value, PASSWORD_VALIDATION_PATTERN):
        if not re.match(PASSWORD_VALIDATION_PATTERN, value):
            raise ValidationError(
                _("Password must contain at least one digit, one lowercase letter, one uppercase letter, one special character, and be at least 8 characters long."),
                code='weak_password'
            )

    # Custom age validation function
    def validate_age(age):
        
        if age < 18:
            raise ValidationError(
                _("You must be 18 years or older to sign up."),
                code='underage'
    )
