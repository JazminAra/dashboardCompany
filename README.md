## AIRTABLE (GRATUITO limitaciones):

## Características:
* Solo acepta 1000 registros en Excel
* Hasta 1GB en cada base de datos
* Hasta 5 solicitudes en la api por segundo

## AIRTABLE CONFIGURAR: El link https://airtable.com/BD_URL/TABLE_URL/URL (distribuido de la BD_URL y de la tabla TABLE_URL 

## API de Airtable: Buscar Airtable rest api docs https://airtable.com/developers/web/api/introduction . Luego  ingresar la BD creada buscar el link del endpoint

## INTEGRA PYHTON CON AIRTABLE:
* Comandos 
```bash
$ python -m pip freeze
$ python -m pip install requests
$ pip install --upgrade pip
$ py -m venv prueba
$ venv\Scripts\activate
$ python main.py
```
* UTILIZAR para EJECUTAR::
```bash
$ cd dashboard
$ prueba\Scripts\activate
$ pip install django
$ python -m django --versión
$ django-admin startproject dashboard
$ python manage.py startapp app

$ pip install pandas
$ pip install plotly

$ python manage.py runserver (ejecutar)
```

* DASBHBOARD PYTHON: Componentes que se utiliza
https://plotly.com/python/ .Primero se debe crear el urls.py para vincularlos con el config.py, luego el views.py son las funciones que le enviamos en el HTML de templates.

