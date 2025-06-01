from django import forms
from .models import Payment, RentalContract

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['contract', 'payment_date', 'amount_paid', 'receipt_file']
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex:1250.00'}),
            'receipt_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'contract': 'Contrato',
            'payment_date': 'Data do Pagamento',
            'amount_paid': 'Valor Pago',
            'receipt_file': 'Arquivo do Recibo (PDF)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['contract'].queryset = RentalContract.objects.filter(owner=user)
