from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

cep_regex = RegexValidator(
    regex=r'^\d{5}-\d{3}$',
    message="O CEP deve estar no formato XXXXX-XXX." 
)
class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_profile', null=True, blank=True)

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
    cpf_cnpj = models.CharField(max_length=18, unique=True, verbose_name="CPF/CNPJ")
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número de Identidade (RG)')

    address = models.CharField(max_length=255, verbose_name="Endereço")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(
        max_length=9,
        verbose_name="CEP", 
        validators=[cep_regex],
    )
    email = models.EmailField(unique=True, verbose_name="E-mail") 
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")

    def __str__(self):
        return self.name
    
    @property
    def first_name(self):
        if self.name:
            return self.name.split(' ')[0]
        return ''

    class Meta:
        verbose_name = "Proprietário" 
        verbose_name_plural = 'Proprietários' 


class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'Casa'),       
        ('apartment', 'Apartamento'), 
        ('kitnet', 'Kitnet'),       
        ('store', 'Loja'),         
        ('garage', 'Garagem'),      
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties', verbose_name="Proprietário") # Label em português
    address = models.CharField(max_length=255, verbose_name="Endereço")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(
        max_length=9,
        verbose_name="CEP", 
    )
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, verbose_name="Tipo de Imóvel") # Label em português
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")  # Novo campo

    def __str__(self):
        return f"{self.property_type.capitalize()} em {self.address}, {self.city}/{self.state}"

    class Meta:
        verbose_name = "Imóvel" 
        verbose_name_plural = "Imóveis" 