from decimal import Decimal
from math import ceil

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .models import (
    Login,
    cotizacion_generada,
    ruta_logistica,
    tarifa_contenedor,
    validate_login_email,
    valida_empresa,
    valida_nombre,
)


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

    rutas = ruta_logistica.objects.order_by('puerto_origen', 'puerto_destino')
    puertos_origen = (
        ruta_logistica.objects.values_list('puerto_origen', flat=True)
        .distinct()
        .order_by('puerto_origen')
    )
    puertos_destino = (
        ruta_logistica.objects.values_list('puerto_destino', flat=True)
        .distinct()
        .order_by('puerto_destino')
    )
    tipos_contenedor = (
        tarifa_contenedor.objects.values_list('tipo_contenedor', flat=True)
        .distinct()
        .order_by('tipo_contenedor')
    )
    context = {
        'rutas': rutas,
        'puertos_origen': puertos_origen,
        'puertos_destino': puertos_destino,
        'tipos_contenedor': tipos_contenedor,
    }

    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente', '').strip()
        empresa = request.POST.get('empresa', '').strip()
        correo_cliente = request.POST.get('correo_cliente', '').strip()
        origen = request.POST.get('puerto_origen', '')
        destino = request.POST.get('puerto_destino', '')
        tipo_contenedor = request.POST.get('tipo_contenedor', '')
        descripcion = request.POST.get('descripcion_carga', '').strip()
        peso = request.POST.get('peso_carga', '').strip()

        try:
            valida_nombre(nombre_cliente)
            valida_empresa(empresa)
            validate_login_email(correo_cliente)
        except ValidationError as error:
            context['error'] = error.messages[0]
            context['form_data'] = request.POST
            return render(request, 'Cotizador/cotizador.html', context)

        try:
            peso_carga = int(peso)
            if peso_carga <= 0:
                raise ValueError
        except (TypeError, ValueError):
            context['error'] = 'Ingresa un peso de carga válido mayor que cero.'
            context['form_data'] = request.POST
            return render(request, 'Cotizador/cotizador.html', context)

        ruta = ruta_logistica.objects.filter(
            puerto_origen=origen,
            puerto_destino=destino,
        ).first()
        tarifa = (
            tarifa_contenedor.objects.filter(
                id_ruta=ruta,
                tipo_contenedor=tipo_contenedor,
            )
            .first()
            if ruta is not None
            else None
        )

        if ruta is None or tarifa is None:
            context['error'] = (
                'No existe una tarifa para la ruta y el contenedor seleccionados.'
            )
            context['form_data'] = request.POST
            return render(request, 'Cotizador/cotizador.html', context)

        cantidad = ceil(peso_carga / tarifa.peso_max)
        costo_fijo = Decimal(tarifa.costo_fijo) * cantidad
        monto_iva = (costo_fijo * Decimal('0.19')).quantize(Decimal('0.01'))
        monto_total = costo_fijo + monto_iva
        context['resultado'] = {
            'ruta': ruta,
            'nombre_cliente': nombre_cliente,
            'empresa': empresa,
            'correo_cliente': correo_cliente,
            'tipo_contenedor': tarifa.tipo_contenedor,
            'descripcion_carga': descripcion,
            'peso_carga': peso_carga,
            'peso_max': tarifa.peso_max,
            'cantidad_contenedores': cantidad,
            'costo_fijo': costo_fijo,
            'monto_iva': monto_iva,
            'monto_total': monto_total,
            'moneda': tarifa.moneda_original,
        }
        request.session['cotizacion_pendiente'] = {
            'id_ruta': ruta.pk,
            'nombre_cliente': nombre_cliente,
            'empresa': empresa,
            'correo_cliente': correo_cliente,
            'descripcion_carga': descripcion,
            'peso_ingresado_kg': peso_carga,
            'tipo_contenedor': tarifa.tipo_contenedor,
            'cantidad_contenedores': cantidad,
            'monto_IVA': int(monto_iva),
            'monto_total': int(monto_total),
        }
        context['form_data'] = request.POST

    return render(request, 'Cotizador/cotizador.html', context)


def informe(request):
    login_id = request.session.get('login_id')
    if login_id is None or not Login.objects.filter(pk=login_id).exists():
        request.session.pop('login_id', None)
        request.session['login_error'] = (
            'Debes iniciar sesión para acceder al informe.'
        )
        return redirect('login')

    cotizacion = request.session.get('cotizacion_pendiente')
    context = {}

    if cotizacion is None:
        context['error'] = (
            'Primero debes calcular una cotización antes de generar el informe.'
        )
        return render(request, 'Cotizador/informe.html', context)

    if request.method == 'POST':
        try:
            registro = cotizacion_generada(
                id_ruta_id=cotizacion['id_ruta'],
                id_usuario_id=login_id,
                nombre_cliente=cotizacion['nombre_cliente'],
                empresa=cotizacion['empresa'],
                correo_cliente=cotizacion['correo_cliente'],
                descripcion_carga=cotizacion['descripcion_carga'],
                peso_ingresado_kg=cotizacion['peso_ingresado_kg'],
                tipo_contenedor=cotizacion['tipo_contenedor'],
                cantidad_contenedores=cotizacion['cantidad_contenedores'],
                monto_IVA=cotizacion['monto_IVA'],
                monto_total=cotizacion['monto_total'],
            )
            registro.full_clean()
            registro.save()
        except ValidationError as error:
            context['error'] = error.messages[0]
            return render(request, 'Cotizador/informe.html', context)

        request.session.pop('cotizacion_pendiente', None)
        context['registro'] = registro

    return render(request, 'Cotizador/informe.html', context)

def historial(request):
    login_id = request.session.get('login_id')
    if login_id is None or not Login.objects.filter(pk=login_id).exists():
        request.session.pop('login_id', None)
        request.session['login_error'] = (
            'Debes iniciar sesión para acceder al historial.'
        )
        return redirect('login')

    historial_cotizaciones = (
        cotizacion_generada.objects.select_related('id_ruta')
        .filter(id_usuario_id=login_id)
        .order_by('-fecha')
    )

    context = {
        'historial_cotizaciones': historial_cotizaciones,
    }

    return render(request, 'Cotizador/historial.html', context)