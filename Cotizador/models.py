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


class Login(models.Model):
    ROL_FIJO = 'Administrador CINTAC'

    #distinto del diagrama que hicimos en el informe.
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(
        max_length=50,
        null=False,
        validators=[validate_login_password],
    )
    email = models.CharField(max_length=100, null=False)
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
