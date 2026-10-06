import re

from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


def validate_login_password(value):
    if len(value) < 8:
        raise ValidationError(
            'La contraseña debe tener al menos 8 caracteres.'
        )
    if not re.search(r'[A-Z]', value):
        raise ValidationError(
            'La contraseña debe contener al menos una mayúscula.'
        )
    if not re.search(r'\d', value):
        raise ValidationError(
            'La contraseña debe contener al menos un número.'
        )

def validate_login_username(value):
    if len(value) < 5:
        raise ValidationError(
            'El nombre de usuario debe tener al menos 5 caracteres.'
        )
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'El nombre de usuario solo puede contener letras, números y guiones bajos.'
        )

def validate_login_email(value):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        raise ValidationError(
            'El correo electrónico no tiene un formato válido.'
        )
        
class Login(models.Model):
    ROL_FIJO = 'Administrador CINTAC'
    
    #distinto del diagrama que hicimos en el informe.
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False, validators=[validate_login_username])
    password = models.CharField(
        max_length=50,
        null=False,
        validators=[validate_login_password],
    )
    email = models.CharField(max_length=100, null=False, validators=[validate_login_email])
    rol = models.CharField(
        max_length=50,
        default=ROL_FIJO,
        editable=False,
        null=False,
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.rol = self.ROL_FIJO
        super().save(*args, **kwargs)

class ruta_logistica(models.Model):
    PUERTOS_ORIGEN = (
        ('Shanghai, China', 'Shanghai, China'),
        ('Ningbo, China', 'Ningbo, China'),
        ('Shenzhen, China', 'Shenzhen, China'),
        ('Qingdao, China', 'Qingdao, China'),
        ('Guangzhou, China', 'Guangzhou, China'),
        ('Tianjin, China', 'Tianjin, China'),
        ('Yokohama, Japon', 'Yokohama, Japon'),
        ('Tokyo, Japon', 'Tokyo, Japon'),
        ('Nagoya, Japon', 'Nagoya, Japon'),
        ('Kobe, Japon', 'Kobe, Japon'),
        ('Osaka, Japon', 'Osaka, Japon'),
        ('Barcelona, España', 'Barcelona, España'),
        ('Los Angeles, EE.UU', 'Los Angeles, EE.UU'),
        ('Callao, Perú', 'Callao, Perú'),
    )
    
    PUERTOS_DESTINO = (
        ('Valparaíso, Chile', 'Valparaíso, Chile'),
        ('San Antonio, Chile', 'San Antonio, Chile'),
    )

    id = models.AutoField(primary_key=True)
    puerto_origen = models.CharField(max_length=100, choices=PUERTOS_ORIGEN, null=False,)
    puerto_destino = models.CharField(max_length=100, choices=PUERTOS_DESTINO, null=False)
    dias_transito = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.puerto_origen} - {self.puerto_destino} ({self.dias_transito} días)"


class tarifa_contenedor(models.Model):
    #PROVEEDORES = (
    #    ('Segucargo', 'Segucargo'),
    #    ('Delpa Group', 'Delpa Group'),
    #)
    
    CONTENEDORES = (
        ('20 HQ', '20 HQ'),
        ('40 HQ', '40 HQ'),
    )
    
    PESOS_MAX = (
        ('20 HQ', 20000),
        ('40 HQ', 25000),
    )

    id = models.AutoField(primary_key=True)
    id_ruta = models.ForeignKey(ruta_logistica, on_delete=models.CASCADE, null=False)
    #embarcador = models.CharField(max_length=100, choices=PROVEEDORES, null=False)
    tipo_contenedor = models.CharField(max_length=50, choices=CONTENEDORES, null=False)
    peso_max = models.IntegerField(choices=PESOS_MAX, null=False)
    costo_fijo = models.IntegerField(null=False)
    moneda_original = models.CharField(max_length=10, default='USD', null=False)

    def __str__(self):
        return f"Tarifas: 20' - {self.contenedor_20}, 40' - {self.contenedor_40}, 40HC - {self.contenedor_40hc}"
    
