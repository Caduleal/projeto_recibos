from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address','city','state','zip_code','property_type','description']
        widgets ={
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'city': forms.TextInput(attrs={'class': 'form-control','placeholder':'Cidade'}),
            'state':forms.TextInput(attrs={'class':'form-control','placeholder':'Estado'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'CEP'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'rows':3, 'placeholder':'Descrição do imóvel: 5 comodos, 1 sala...'})
        }
        labels ={
            'address':'Endereço',
            'city':'Cidade',
            'state':'Estado',
            'zip_code':'CEP',
            'property_type':'Tipo de Imóvel',
            'description': 'Descrição'

        }