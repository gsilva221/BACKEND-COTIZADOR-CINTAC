from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cotizador', '0005_alter_login_email_alter_login_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruta_logistica',
            name='puerto_origen',
            field=models.CharField(
                choices=[
                    ('Shanghai, China', 'Shanghai, China'),
                    ('Ningbo, China', 'Ningbo, China'),
                    ('Shenzhen, China', 'Shenzhen, China'),
                    ('Qingdao, China', 'Qingdao, China'),
                    ('Guangzhou, China', 'Guangzhou, China'),
                    ('Tianjin, China', 'Tianjin, China'),
                    ('Yokohama, Japon', 'Yokohama, Japon'),
                    ('Tokyo, Japon', 'Tokyo, Japon'),
                    ('Nagoya, Japon', 'Nagoya, Japon'),
                    ('Kobe, Japon', 'Kobe, Japon'),
                    ('Osaka, Japon', 'Osaka, Japon'),
                    ('Barcelona, España', 'Barcelona, España'),
                    ('Los Angeles, EE.UU', 'Los Angeles, EE.UU'),
                    ('Callao, Perú', 'Callao, Perú'),
                ],
                max_length=100,
            ),
        ),
    ]
