from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from properties.models import Owner

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    name = forms.CharField(max_length=200, label="Nome Completo", required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'email', 'username')
        widgets = {
            'username': forms.HiddenInput()
        }

    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        owner = Owner.objects.create(
            user=user,
            name=self.cleaned_data['name'], 
            email=self.cleaned_data['email']
        )
        return user

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        exclude = ('user', 'name', 'email',)
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
        