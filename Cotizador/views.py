from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'Cotizador/login.html')