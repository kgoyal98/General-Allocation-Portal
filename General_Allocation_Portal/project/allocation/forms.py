## Form Used for Registration
from django import forms
from allocation.models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

## Registration Form
# Registration form used to register new institutes to allow using our services
class InstiForm(UserCreationForm):
    ## Metadata
    class Meta:
        model = User #< Form to create new user model
        fields = ['username', 'password1', 'password2', ] #< Fields to be taken input