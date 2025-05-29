from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome Completo")
    nationality = models.CharField(max_length=100, verbose_name="Nacionalidade", default='Brasileiro')
    profession = models.CharField(max_length=100, verbose_name='Profissão', blank=True, null=True)
    civil_status = models.CharField(
        max_length=50,
        choices=[
            ('single', 'Solteiro(a)'),
            ('married', 'Casado(a)'),
            ('divorced', 'Divorciado(a)'),
            ('widowed', 'Viúvo(a)'),
            ('union', 'União Estável'),
        ],
        verbose_name='Estado Civil',
        blank=True,
        null=True
    )
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número de Identidade (RG)')
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Inquilino"
        verbose_name_plural = 'Inquilinos'