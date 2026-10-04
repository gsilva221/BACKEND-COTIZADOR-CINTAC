from django.contrib import admin
from Cotizador.models import Login

# Register your models here.
@admin.register(Login)
class loginAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol')
    search_fields = ('username', 'rol')
    list_filter = ('rol',)
    ordering = ('id',)
    