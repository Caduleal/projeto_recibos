from django import forms
from .models import Tenant
class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'nationality', 'civil_status', 'cpf', 'rg', 'email', 'phone', 'profession']

        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome completo do inquilino'}), 
            'cpf': forms.TextInput(attrs={'class': 'form-control','placeholder':'Ex: 123.456.789-00'}), 
            'rg': forms.TextInput(attrs={'class':'form-control','placeholder':'RG (opcional)'}), 
            'phone_number': forms.TextInput(attrs={'class':'form-control','placeholder':'Ex: (DD) 91234-5678'}), 
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':3,'placeholder':'Endereço completo'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Brasileiro(a)'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'profissao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Engenheiro(a)'}),
        }
        labels ={
            'name': 'Nome do Inquilino', 
            'cpf': 'CPF', 
            'rg': 'RG',
            'phone_number': 'Telefone', 
            'address': 'Endereço',
            'city': 'Cidade',
            'state': 'Estado',
            'zip_code': 'CEP',
            'nacionalidade': 'Nacionalidade',
            'estado_civil': 'Estado Civil',
            'profissao': 'Profissão',
        }
    
