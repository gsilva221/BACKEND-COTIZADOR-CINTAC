from django.db import models

# Create your models here.
class Login(models.Model):
    ROL_FIJO = 'Administrador CINTAC'

    #distinto del diagrama que hicimos en el informe.
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
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
