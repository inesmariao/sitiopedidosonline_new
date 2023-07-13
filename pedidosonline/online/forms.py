from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegistroClienteForm(forms.Form):
    nombres = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=70, required=True)
    password = forms.CharField(max_length=50, required=True)
    confirmar_password = forms.CharField(max_length=50, required=True)

    # personalizar la validación
    def clean(self):
        clean_data = super().clean()
        password = clean_data.get("password")
        confirmar_password = clean_data.get("confirmar_password")
        email = clean_data.get("email")

        # 1: el campo contraseña y confirmar contraseña sean iguales
        if password != confirmar_password:
            self.add_error("password", "Las contraseñas no coinciden")
            self.add_error("confirmar_password", "Las contraseñas no coinciden")

        #2: no se permita el registro de un cliente con un correo existente en la base de datos
        # auth_usaer => User
        coincidencias = User.objects.filter(username=email).count()
        if coincidencias > 0:
            self.add_error("email", "Correo electrónico está en uso por otro usuario")
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=80, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput())


    def clean(self):
        data = super().clean()
        email = data.get("email")
        password = data.get("password")

        # 01: Validar que los datos sean correctos
        usuario_logeado = authenticate(username=email, password=password)

        if usuario_logeado is None:
            self.add_error("email", "Datos de inicio de sesión son incorrectos")