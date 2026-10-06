from django.contrib import admin
from django import forms
from Cotizador.models import Login, ruta_logistica, tarifa_contenedor

# Register your models here.
class LoginAdminForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(render_value=False),
        }


@admin.register(Login)
class loginAdmin(admin.ModelAdmin):
    form = LoginAdminForm
    list_display = ('id','username', 'email', 'rol')
    search_fields = ('username', 'rol')
    list_filter = ('rol',)
    ordering = ('id',)

@admin.register(ruta_logistica)
class ruta_logisticaAdmin(admin.ModelAdmin):
    list_display = ('id', 'puerto_origen', 'puerto_destino', 'dias_transito')
    search_fields = ('puerto_origen', 'puerto_destino')
    list_filter = ('puerto_origen', 'puerto_destino')
    ordering = ('id',)

@admin.register(tarifa_contenedor)
class tarifa_contenedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_contenedor', 'costo_fijo', 'id_ruta')
    search_fields = ('tipo_contenedor', 'id_ruta')
    list_filter = ('tipo_contenedor', 'id_ruta')
    ordering = ('id',)