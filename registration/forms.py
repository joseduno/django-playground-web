from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control mt-3', 'rows': '3', 'placeholder': 'Biografía'
            }),
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Enlace'}),
        }
        labels = {
            'avatar': '', 'bio': '', 'link': ''
        }


class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, help_text='Requerido, 254 catacteres como máximo y debe ser válido',
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:  # Para verificar si se ha modificado el campo
            if User.objects.filter(email=email).exists():  # verificando si existe el email
                raise forms.ValidationError('El mail ya existe, prueba con otro')
        return email