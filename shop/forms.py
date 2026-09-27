from django import forms
from django.contrib.auth import get_user_model
from .models import Order
CustomUser = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'door_number', 'postal_code', 'locality']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está registado.")
        return email

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password_confirm'):
            raise forms.ValidationError("As palavras-passe não coincidem.")
        return cd.get('password_confirm')
    
class CheckoutForm(forms.ModelForm):
    door_number = forms.CharField(max_length=20, required=False, label="Nº de Porta")
    postal_code = forms.CharField(max_length=20, required=True, label="Código Postal")
    locality = forms.CharField(max_length=100, required=True, label="Localidade")

    class Meta:
        model = Order
        fields = ['customer_name', 'email', 'address', 'payment_method']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'door_number', 'postal_code', 'locality']
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Último Nome',
            'username': 'Nome de Utilizador',
            'email': 'E-mail',
            'phone': 'Telefone',
            'address': 'Morada',
            'door_number': 'Nº de Porta',
            'postal_code': 'Código Postal',
            'locality': 'Localidade',
        }