from django import forms


class RegistroClienteForm(forms.Form):
    nombres = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=70, required=True)
    password = forms.CharField(max_length=50, required=True)
    confirmar_password = forms.CharField(max_length=50, required=True)
    

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=80, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())