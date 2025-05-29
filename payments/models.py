from django.db import models
from contracts.models import RentalContract


class Payment(models.Model):
    contract = models.ForeignKey(RentalContract, on_delete=models.CASCADE, related_name='payments', verbose_name="Contrato")
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    payment_date = models.DateField(verbose_name="Data do Pagamento")
    reference_month = models.IntegerField(verbose_name="Mês de Referência", help_text="Mês ao qual o pagamento se refere (1=Jan, 12=Dez)")
    reference_year = models.IntegerField(verbose_name="Ano de Referência", help_text="Ano ao qual o pagamento se refere (Ex: 2025)")
    receipt_file = models.FileField(upload_to='receipts_pdf/', blank=True, null=True, verbose_name="Arquivo do Recibo (PDF)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-payment_date', '-created_at']
        unique_together = ('contract', 'reference_month', 'reference_year')