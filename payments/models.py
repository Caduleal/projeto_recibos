from django.db import models
from contracts.models import RentalContract
import calendar
from datetime import date 


class Payment(models.Model):
    contract = models.ForeignKey(RentalContract, on_delete=models.CASCADE, related_name='payments', verbose_name="Contrato")
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    payment_date = models.DateField(verbose_name="Data do Pagamento")
    reference_month = models.IntegerField(verbose_name="Mês de Referência" )
    reference_year = models.IntegerField(verbose_name="Ano de Referência")
    receipt_file = models.FileField(upload_to='receipts_pdf/', blank=True, null=True, verbose_name="Arquivo do Recibo (PDF)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-payment_date', '-created_at']
        unique_together = ('contract', 'reference_month', 'reference_year')

    def __str__(self):
        return f"Pagamento de R${self.amount_paid:.2f} para {self.contract.property.address} ({self.reference_month}/{self.reference_year})"

    def get_payment_status(self):
        try:
            last_day_of_ref_month = calendar.monthrange(self.reference_year, self.reference_month)[1]
            actual_due_day = min(self.contract.due_day, last_day_of_ref_month)
            expected_due_date = date(self.reference_year, self.reference_month, actual_due_day)
        except (ValueError, TypeError):
            return {'text': 'Data de Vencimento Inválida', 'style_key': 'status_invalid'}

        if self.payment_date <= expected_due_date:
            return {'text': 'Pago em Dia', 'style_key': 'status_on_time'}
        else:
            return {'text': 'Pago com Atraso', 'style_key': 'status_delayed'}
