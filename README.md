# Práctica 1: Web Scraping

## Descripción
En este repositorio se presenta el material realizado bajo el contexto de la Práctica 1 de la asignatura 'Tipología y Ciclo de Vida de los Datos' del Máster en Ciencia de Datos de la Universitat Oberta de Catalunya.

Durante la misma, se ha desarrollado una herramienta que permite obtener datos sobre anuncios de coches publciados en www.milanuncios.com utilizando técnicas de __web scraping__ haciendo uso del lenguaje de programación Python, su libraría Beautiful Soup y Selenium. 

## Componentes del equipo
- Pablo Campillo Sánchez
- Pedro Uceda Martínez

## Conjunto de datos

El conjunto de datos que genera la herramienta se sitúa en un fichero de salida .CSV con las siguientes características:

- **ad_id**: Identificador del anuncio del coche.
- **ad_type**: Tipo de anuncio. En nuestro caso, siempre va a ser Oferta.
- **ad_time**: Tiempo que llevaba publicado el anuncio cuando se recogió la información, en formato X horas o X días. En el caso en que fuese un anuncio destacado, no tenemos esa información.
- **ad_title**: Título del anuncio de venta, con formato {Marca} – {Modelo}.
- **car_desc**: Preview de la descripción del anuncio de venta del vehículo.
- **car_km**: Kilómetros que tiene recorridos el coche.
- **car_year**: Año de matriculación del vehículo.
- **car_engine_type**: Tipo de transmisión. Posibles valores: Manual | Automático.
- **car_door_num**: Número de puertas de las que dispone el coche.
- **car_power**: Potencia del vehículo, en formato XXX CV.
- **car_price**: Precio en euros por el que se vende el coche.
- **advertizer_type**: Indica cuál es el tipo de vendedor del vehículo. Valores posibles: Profesional | Particular.
- **image_url**: Foto principal del anuncio de venta del coche.
- **ts**: Hora en la que se recogió la información, con formato YYYY-MM-DD hh:mm:ss.ms.
- **region**: Provincia en la que se está vendiendo el vehículo.
    

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
