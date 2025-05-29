from django.db import models
from properties.models import Property, Owner
from datetime import date
from tenants.models import Tenant

class RentalContract(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='rental_contracts',verbose_name='Property')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='rental_contracts', verbose_name="Tenant")
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE, related_name='owner_contracts', verbose_name="Owner")

    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date") 
    due_day = models.IntegerField(default=10, verbose_name="Due Day", help_text="Day of the month the rent is due (e.g., 10 for the 10th)")
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rent Amount")
    contract_file = models.FileField(upload_to='contracts_pdf/', blank=True, null=True, verbose_name="Contract File (PDF)")

    STATUS_CHOICES = [
    ('active', 'Ativo'),
    ('closed', 'Encerrado'),
    ('pending', 'Pendente'),
]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Status do Contrato")
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Contrato de {self.tenant.name} para {self.property.address}"

    class Meta:
        verbose_name = "Contrato de Aluguel"
        verbose_name_plural = "Contratos de Aluguel"
        ordering = ['-start_date']