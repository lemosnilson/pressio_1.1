from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    terms = forms.BooleanField(
        required=True,
        label="Eu aceito os Termos e Condições",
        error_messages={'required': 'Você deve aceitar os Termos e Condições para se cadastrar.'}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "terms")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email
