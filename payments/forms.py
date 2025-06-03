from django import forms
from decimal import Decimal, InvalidOperation
from .models import Payment, RentalContract
from properties.models import Owner


class PaymentForm(forms.ModelForm):
    reference_input = forms.CharField(
        label="Mês de Referência",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/AAAA',
            'pattern': '(0[1-9]|1[0-2])/20[2-9][0-9]',
            'title': 'Informe no formato MM/AAAA',
        })
    )

    class Meta:
        model = Payment
        fields = ['contract', 'amount_paid', 'payment_date', 'reference_input']
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1250.00'}),
        }
        labels = {
            'contract': 'Contrato',
            'payment_date': 'Data do Pagamento',
            'amount_paid': 'Valor Pago',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                owner = Owner.objects.get(user=user)
                self.fields['contract'].queryset = RentalContract.objects.filter(property__owner=owner)
            except Owner.DoesNotExist:
                self.fields['contract'].queryset = RentalContract.objects.none()

    def clean_reference_input(self):
        data = self.cleaned_data['reference_input']
        try:
            month_str, year_str = data.split('/')
            month = int(month_str)
            year = int(year_str)
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            raise forms.ValidationError("Informe o mês de referência no formato MM/AAAA válido.")
        return month, year

    def clean_amount_paid(self):
        value = self.cleaned_data['amount_paid']
        if isinstance(value, str):
            value = value.replace('R$', '').replace('.', '').replace(',', '.').strip()
            try:
                value = Decimal(value)
            except InvalidOperation:
                raise forms.ValidationError('Informe um valor numérico válido.')
        if value < 0:
            raise forms.ValidationError('O valor pago não pode ser negativo.')
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)

        month, year = self.cleaned_data.get('reference_input', (None, None))
        instance.reference_month = month
        instance.reference_year = year

        if commit:
            instance.save()
        return instance
