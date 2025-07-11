from django.db import models
from datetime import datetime 


## Cadastro de Clientes     
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return "{} - {}".format(self.name, self.email)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


## Opções de Imóveis
class TypeImmobile(models.TextChoices):
    APARTMENT = 'APARTAMENTO','APARTAMENTO'
    KITNET = 'KITNET','KITNET'
    HOUSE = 'CASA','CASA' 


## Cadastro de Imóveis
class Immobile(models.Model):
    code = models.CharField(max_length=100)
    type_item = models.CharField(max_length=100, choices=TypeImmobile.choices)
    address = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    is_locate = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.code, self.type_item)
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-id']


## Cadastrar as Imagens do Imóvel
class ImmobileImage(models.Model):
    image = models.ImageField('Images',upload_to='images')
    immobile = models.ForeignKey(Immobile, related_name='immobile_images', on_delete=models.CASCADE)
 
    def __str__(self):
        return self.immobile.code 


## Registrar Locação
class RegisterLocation(models.Model):
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE, related_name='reg_location')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    dt_start = models.DateTimeField('Inicio')
    dt_end = models.DateTimeField('Fim')
    """ SETA AUTOMATICO A DATA SELECIONADA ACIMA, com o datetime """
    create_at = models.DateField(default=datetime.now, blank=True)
    
    def __str__(self):
        return "{} - {}".format(self.client, self.immobile)
    
    class Meta:
        verbose_name = 'Registrar Locação'
        verbose_name_plural = 'Registrar Locação'
        ordering = ['-id']

#Contratooo
class Contract(models.Model):
    register_location = models.OneToOneField('RegisterLocation', on_delete=models.CASCADE, related_name='contract')
    document = models.FileField(upload_to='contracts/', verbose_name="Documento do Contrato")
    signed_date = models.DateField(verbose_name="Data de Assinatura")

    def __str__(self):
        return f"Contrato - {self.register_location}"

    class Meta:
        verbose_name = 'Contrato de Aluguel'
        verbose_name_plural = 'Contratos de Aluguel'
        ordering = ['-id']

#Pagamento
class Payment(models.Model):
    register_location = models.ForeignKey('RegisterLocation', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    payment_date = models.DateField(verbose_name="Data do Pagamento")
    
    class PaymentMethod(models.TextChoices):
        PIX = 'PIX', 'PIX'
        BOLETO = 'BOLETO', 'Boleto'
        CARTAO = 'CARTAO', 'Cartão'
        DINHEIRO = 'DINHEIRO', 'Dinheiro'

    method = models.CharField(max_length=20, choices=PaymentMethod.choices, verbose_name="Forma de Pagamento")

    def __str__(self):
        return f"{self.register_location} - R${self.amount} ({self.method})"

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-payment_date']

#Funcionario
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50)  # exemplo: "Corretor", "Gerente", etc.

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['-id']

#vISITAS
class VisitStatus(models.TextChoices):
    AGENDADA = 'AGENDADA', 'Agendada'
    REALIZADA = 'REALIZADA', 'Realizada'
    CANCELADA = 'CANCELADA', 'Cancelada'

class VisitSchedule(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='visits')
    immobile = models.ForeignKey(Immobile, on_delete=models.CASCADE, related_name='visits')
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='visits')
    date = models.DateTimeField(verbose_name='Data da Visita')
    status = models.CharField(max_length=20, choices=VisitStatus.choices, default=VisitStatus.AGENDADA)

    def __str__(self):
        return f"Visita de {self.client.name} - {self.immobile.code} em {self.date.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'Agendamento de Visita'
        verbose_name_plural = 'Agendamentos de Visitas'
        ordering = ['-date']

#Manutenção
class MaintenanceStatus(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente'
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em andamento'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'

class MaintenanceRequest(models.Model):
    register_location = models.ForeignKey(RegisterLocation, on_delete=models.CASCADE, related_name='maintenances')
    description = models.TextField('Descrição do problema')
    request_date = models.DateField(default=datetime.now)
    status = models.CharField(max_length=20, choices=MaintenanceStatus.choices, default=MaintenanceStatus.PENDENTE)

    def __str__(self):
        return f"Manutenção - {self.register_location.immobile.code} ({self.status})"

    class Meta:
        verbose_name = 'Solicitação de Manutenção'
        verbose_name_plural = 'Solicitações de Manutenção'
        ordering = ['-request_date']


#Propprietario
class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Proprietário'
        verbose_name_plural = 'Proprietários'
        ordering = ['-id']




