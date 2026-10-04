# Cotizador Logístico Interno CINTAC

## Descripción
Sistema desarrollado para uso interno exclusivo de la empresa CINTAC. Esta herramienta permite simular cotizaciones de importación marítima, calculando costos de flete, tiempos de tránsito y la asignación automática de contenedores (20' y 40' HQ) según el peso de la carga. 

El sistema utiliza como base de datos maestra una planilla de Excel administrada directamente por los analistas internos de la empresa.

## Características Principales
- **Cálculo de Contenedores:** Asignación automática considerando topes viales de 20 y 25 toneladas.
- **Lectura de Datos Maestros:** Extracción de tarifas desde archivo Excel local (proyectado a OneDrive corporativo).
- **Control de Acceso:** Uso cerrado y exclusivo para un máximo de 3 administradores internos.
- **Interfaz Corporativa:** Diseño alineado al manual de marca y colores institucionales de CINTAC.

## Tecnologías Utilizadas
- **Backend / Frontend:** Python 3, Django, Django Templates.
- **Procesamiento de Datos:** Pandas / Openpyxl (para lectura del Excel maestro).
- **Seguridad:** Autenticación local y control de sesiones en esta fase de prototipo.

## Instalación y Ejecución (Entorno Local)

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd cotizador-cintac

```

2. **Crear y activar un entorno virtual:**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

```


3. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```


4. **Configurar el archivo maestro:**
Asegúrate de que el archivo Excel de tarifas (`tarifas_cintac.xlsx`) esté ubicado en la carpeta raíz o en la ruta definida en las configuraciones del proyecto.
5. **Ejecutar las migraciones y el servidor de desarrollo:**
```bash
python manage.py migrate
python manage.py runserver

```


6. **Acceder a la aplicación:**
Abre tu navegador web e ingresa a `http://localhost:8000`.

