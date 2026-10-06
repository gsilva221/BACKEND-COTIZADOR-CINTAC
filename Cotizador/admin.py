from django.contrib import admin
from django import forms
from Cotizador.models import Login, ruta_logistica, tarifa_contenedor, cotizacion_generada

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
    
@admin.register(cotizacion_generada)
class cotizacion_generadaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_ruta', 'id_usuario', 'fecha', 'nombre_cliente', 'empresa', 'correo_cliente', 'descripcion_carga', 'peso_ingresado_kg', 'tipo_contenedor', 'cantidad_contenedores', 'monto_IVA', 'monto_total')
    search_fields = ('id_ruta__puerto_origen', 'id_ruta__puerto_destino', 'id_usuario__username', 'nombre_cliente', 'empresa')
    list_filter = ('id_ruta__puerto_origen', 'id_ruta__puerto_destino', 'id_usuario__username')
    ordering = ('-fecha',)
    
