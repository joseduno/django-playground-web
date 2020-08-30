from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text='Requerido, 254 catacteres como máximo y debe ser válido',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    # Para validar campos
    def clean_email(self):
        email = self.cleaned_data.get('email')  # obtener email del formulario
        if User.objects.filter(email=email).exists():  # verificando si existe el email
            raise forms.ValidationError('El mail ya existe, prueba con otro')
        return email
