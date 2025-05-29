from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from properties.models import Owner

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        exclude = ('user', 'email', 'phone', 'rg',)
        fields = UserCreationForm.Meta.fields + ('email',)

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        exclude = ('user',) 
        labels = {
            'name': 'Nome Completo',
            'nationality': 'Nacionalidade',
            'profession': 'Profissão',
            'civil_status': 'Estado Civil',
            'cpf_cnpj': 'CPF/CNPJ',
            'rg': 'Número de Identidade (RG)',
            'address': 'Endereço',
            'complement': 'Complemento',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
            'zip_code': 'CEP',
            'email': 'E-mail de Contato',
            'phone': 'Telefone de Contato',
        }
        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={'placeholder': 'Ex: 123.456.789-00 ou 12.345.678/0001-90'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Ex: 12345-678'}),
        
        }