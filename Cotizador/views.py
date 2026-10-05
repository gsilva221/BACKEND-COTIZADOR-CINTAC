from django.shortcuts import redirect, render

from .models import Login


def login(request):
    error = request.session.pop('login_error', None)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        account = Login.objects.filter(
            username=username,
            password=password,
        ).first()

        if account is not None:
            request.session['login_id'] = account.pk
            return redirect('cotizador')

        return render(
            request,
            'Cotizador/login.html',
            {'error': 'Usuario o contraseña incorrectos.'},
        )

    return render(request, 'Cotizador/login.html', {'error': error})


def Cotizador(request):
    login_id = request.session.get('login_id')
    if login_id is None or not Login.objects.filter(pk=login_id).exists():
        request.session.pop('login_id', None)
        request.session['login_error'] = (
            'Debes iniciar sesión para acceder al cotizador.'
        )
        return redirect('login')

    return render(request, 'Cotizador/cotizador.html')
