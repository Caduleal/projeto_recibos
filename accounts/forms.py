from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from properties.models import Owner


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    name = forms.CharField(max_length=200, label="Nome Completo", required=True)

    password1 = forms.CharField(
    label="Senha",
    widget=forms.PasswordInput(attrs={'class': 'form-control password-input'}) 
)


    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control password-input'}) 
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'email', 'password1', 'password2', 'username')
        widgets = {
            'username': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'username' in self.fields:
            self.fields['username'].required = False
            self.fields['username'].widget = forms.HiddenInput()

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            cleaned_data['username'] = email
        return cleaned_data

    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']

        if commit:
            user.save()
        return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True,label='Email de Acesso')
    full_name = forms.CharField(max_length=255,required=False,label="Nome Completo")

    class Meta:
        model = User
        fields = ['full_name','email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso por outro usuário.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '').strip()
        name_parts = full_name.split(' ', 1) 
        user.first_name = name_parts[0] if name_parts else ''
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'] 
        if commit:
            user.save()
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
        