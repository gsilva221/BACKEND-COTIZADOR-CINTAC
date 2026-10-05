from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Login, validate_login_password


class LoginViewTests(TestCase):
    def setUp(self):
        self.account = Login.objects.create(
            username='usuario-prueba',
            password='Clave123',
            email='usuario@example.com',
        )

    def test_invalid_credentials_are_rejected(self):
        response = self.client.post(
            '/Cotizador/login/',
            {'username': 'usuario-prueba', 'password': 'Incorrecta1'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos.')
        self.assertNotIn('login_id', self.client.session)

    def test_valid_credentials_redirect_to_cotizador(self):
        response = self.client.post(
            '/Cotizador/login/',
            {'username': 'usuario-prueba', 'password': 'Clave123'},
        )

        self.assertRedirects(response, '/Cotizador/cotizador/')
        self.assertEqual(self.client.session['login_id'], self.account.pk)

    def test_cotizador_requires_an_authenticated_session(self):
        response = self.client.get('/Cotizador/cotizador/')

        self.assertRedirects(response, '/Cotizador/login/')

    def test_direct_cotizador_access_shows_login_error(self):
        response = self.client.get('/Cotizador/cotizador/', follow=True)

        self.assertContains(
            response,
            'Debes iniciar sesión para acceder al cotizador.',
        )

    def test_password_requires_uppercase_number_and_eight_characters(self):
        for password in ('corta1A', 'solamente8', 'Solamente'):
            with self.subTest(password=password):
                with self.assertRaises(ValidationError):
                    validate_login_password(password)

        validate_login_password('Valida123')
