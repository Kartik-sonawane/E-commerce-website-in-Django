from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer

# Registration Form
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control mt-4', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'form-control mt-4', 'placeholder': 'Confirm Password'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control mt-4', 'placeholder': 'Email'}))
    class Meta :
        model = User
        fields =['username', 'email', 'password1', 'password2']
        # labels = {
        #     'username':'User Name',
        #     'email': 'Email',
        # }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control mt-3','placeholder': 'User Name'}),
        }


# Login Form
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control ', 'placeholder':'User Name'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete':'current-password', 'class':'form-control ', 'placeholder': 'Password'}))


# Password Change
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete':'current-password','autofocus':True,'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control ',
               'placeholder': 'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password','class': 'form-control',
               'placeholder': 'Confirm New Password'}))


# Password Reset
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Email' }))

# Set Password
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control ',
               'placeholder': 'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password','class': 'form-control',
               'placeholder': 'Confirm New Password'}))


# Profile Form
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields =['name', 'locality', 'city', 'state', 'zipcode']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control mt-4', 'placeholder': 'Name'}),
            'locality':forms.TextInput(attrs={'class':'form-control mt-4', 'placeholder': 'Locality'}),
            'city':forms.TextInput(attrs={'class':'form-control mt-4', 'placeholder': 'City'}),
            'state':forms.Select(attrs={'class':'form-control mt-4', 'placeholder': 'State'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control mt-4', 'placeholder': 'ZipCode'}),
        }