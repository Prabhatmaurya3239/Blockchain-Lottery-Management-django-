# lottery_app/forms.py

from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'date_of_birth', 'phone_number', 'address', 'password', 'walet_address']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password != re_password:
            raise forms.ValidationError("Passwords do not match")

class LoginForm(forms.Form):
    wallet_address = forms.CharField(max_length=42)
    email_or_phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ForgetPasswordForm(forms.Form):
    email_or_phone = forms.CharField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)
