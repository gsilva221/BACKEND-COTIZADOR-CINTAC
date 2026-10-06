from django.urls import path
from Cotizador.views import Cotizador, informe, login, historial

urlpatterns = [
    path('login/', login, name='login'),
    path('cotizador/', Cotizador, name='cotizador'),
    path('informe/', informe, name='informe'),
    path('historial/', historial, name='historial'),
]