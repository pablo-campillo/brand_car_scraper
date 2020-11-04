# Introducción
Herramienta para obtener características de anuncios de coches publicados en www.milanuncios.com con fines totalmente académicos.

La herramienta se ha desarrollado en el contexto de una práctica de la asignatura 'Tipología y ciclo de vida de los datos' 
del Máster Ciencia de Datos de la www.ouc.edu.

## Conjunto de datos
El conjunto de datos que genera es un csv con las siguientes características:
- ad_id: Identificador del anuncio del coche.
- ad_type: Tipo de anuncio. Será simpre "Oferta".
- ad_time: Tiempo que llevaba publicado el anuncio cuando se recogió la información, en formato X horas o X días. En el caso en que fuese un anuncio destacado, no tenemos esa información.
- ad_title: Título del anuncio de venta, con formato {Marca} – {Modelo}
- car_desc: Descripción (parte de la misma) del vehículo.
- car_km: Kilómetros que tiene recorridos el coche
- car_year: Año de matriculación del vehículo
- car_engine_type: Tipo de transmisión. Posibles valores: Manual | Automático.
- car_door_num: Número de puertas de las que dispone el coche
- car_power: Potencia del vehículo, en formato XXX CV
- car_price: Precio en euros por el que se vende el coche
- advertizer_type: Profesional o Particular
- image_url: Foto principal del anuncio de venta del coche
- ts: Fecha y hora en la que se recogió la información, con formato YYYY-MM-DD hh:mm:ss.ms
- region: Region española a la que pertenece el vehículo

# Equipo
- Pedro Uceda Martinez
- Pablo Campillo Sánchez

# Content

# Instalación

Desde el directorio raíz:
```
$ python setup.py install
```

Es necesario instalar el driver correspondiente a tu navegador para selenium: https://www.selenium.dev/downloads/

# Uso

```bash
Usage: scrap [OPTIONS] OUTPUT_FILE

  This tool scraps list of second car ads on https://www.milanuncios.com/coches-de-segunda-mano-en-<province>/?orden=relevance&fromSearch=<page_number> where <region> is the name of a region in Spain (madrid, andalucia, murcia) and <page_number> is an integer greater or equal than 1. By searching for cars by regions we are able to save where they are being sold.

  If no OPTIONS are provided all the pages will be parsed.

  OUTPUT_FILE a path where the csv file will be stored.

  Examples:
        - For scraping from page 1 to the end, region madrid:
            $ scrap out.csv
        - For scraping from page 1 to 10, region madrid:
            $ scrap --tp 10 out.csv
        - For scraping from page 5 to 10, region madrid:
            $ scrap -fp 5 -tp 10 out.csv
        - For scraping from page 5, region madrid:
            $ scrap -fp 5 out.csv
        - For scraping from page 5 to 10, region murcia:
            $ scrap -fp 5 -tp 10 --region murcia out.csv


  AUTHORS:
      - Pedro Uceda Martinez
      - Pablo Campillo Sánchez

Options:
  --fp INTEGER   First page to be parsed. Default value is 1.
  --tp INTEGER   Last page to be parsed, i.e. until the last page.
  --region TEXT  Region to be parsed e.g. madrid.
  --help         Show this message and exit.
  
```

# Entorno de desarrollo

Crear un entorno virtual:
```bash
$ python3 -m venv <env_directory> python=3.8
```

Activar el entonro:
```bash
$ source <env_directory>/bin/activate
```

Instalar las librerías y sus dependencias como referencia al directorio:
```bash
$ python setup.py develop
```
