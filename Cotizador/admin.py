from django.contrib import admin
from django import forms
from Cotizador.models import Login

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
    list_display = ('username', 'email', 'rol')
    search_fields = ('username', 'rol')
    list_filter = ('rol',)
    ordering = ('id',)
    