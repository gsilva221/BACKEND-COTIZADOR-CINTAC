from django.urls import path
from Cotizador.views import login

urlpatterns = [
    path('login/', login),
]