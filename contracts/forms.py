from django import forms
from .models import RentalContract, Tenant, Property 

class ContractForm(forms.ModelForm):
    class Meta:
        model = RentalContract
        fields = ['tenant', 'property', 'rent_amount', 'start_date', 'end_date', 'due_day', 'status', 'contract_text']
        widgets = {
            'tenant': forms.Select(attrs={'class':'form-control'}),
            'property': forms.Select(attrs={'class': 'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ex: 1250.00'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 5 (para o dia 5)'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'contract_text': forms.Textarea(attrs={'class':'form-control','rows':5,'placeholder':'Cláusulas contratuais (opcional)'}),
        }
        labels = {
            'tenant': 'Inquilino',
            'property': 'Imóvel',
            'rent_amount': 'Valor do Aluguel',
            'start_date': 'Data de Início',
            'end_date': 'Data de Fim',
            'due_day': 'Dia de Vencimento',
            'status': 'Status',
            'contract_text': 'Cláusulas Contratuais',
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tenant'].queryset = Tenant.objects.all()
            self.fields['property'].queryset = Property.objects.filter(owner=user.owner_profile)
