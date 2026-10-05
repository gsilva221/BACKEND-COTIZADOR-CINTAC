from django.urls import path
from Cotizador.views import login, Cotizador

urlpatterns = [
    path('login/', login, name='login'),
    path('cotizador/', Cotizador, name='cotizador'),
]