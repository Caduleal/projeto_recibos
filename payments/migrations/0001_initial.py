# Generated by Django 5.2.1 on 2025-05-29 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor Pago')),
                ('payment_date', models.DateField(verbose_name='Data do Pagamento')),
                ('reference_month', models.IntegerField(help_text='Mês ao qual o pagamento se refere (1=Jan, 12=Dez)', verbose_name='Mês de Referência')),
                ('reference_year', models.IntegerField(help_text='Ano ao qual o pagamento se refere (Ex: 2025)', verbose_name='Ano de Referência')),
                ('receipt_file', models.FileField(blank=True, null=True, upload_to='receipts_pdf/', verbose_name='Arquivo do Recibo (PDF)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado Em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='contracts.rentalcontract', verbose_name='Contrato')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
                'ordering': ['-payment_date', '-created_at'],
                'unique_together': {('contract', 'reference_month', 'reference_year')},
            },
        ),
    ]
