from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from authentication.models import CustomUser
from customer.models import Customer
from driver.models import Driver



class CustomerSignupForm (UserCreationForm):

    Preferred_method = forms.ChoiceField(
        choices = Customer.payment_methods,
        widget=forms.RadioSelect,
        required=False
    )
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email','first_name','last_name','birthdate','image','phone_no')
        

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.preferred_method = self.Preferred_method  
        return user
    

class DriverSignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email','first_name','last_name','birthdate','image','phone_no')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_driver = True
        user.save() 
        driver = Driver.objects.create(user=user) 
        return user

