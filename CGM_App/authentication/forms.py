from django import forms


class LoginForm(forms.Form):
    input_username = forms.CharField(label='input_username')
    input_password = forms.CharField(label='input_password')
