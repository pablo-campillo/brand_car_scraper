# Introduction
A scraper tool that aims at gathering features and pictures of vehicles from www.milanuncios.com in order to develop AI  models related with the given domain such as a brand model classifier, among others.

The tool is developed in the context of a task for the 'Tipología y ciclo de vida de los datos' subject of the Data Science Master at UOC Univeristy.

# Team
- Pedro Uceda Martinez
- Pablo Campillo Sánchez

# Content

# Installation

From the root directory:
```
$ python setup.py install
```

# Usage

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

# Set up dev environment

Create a python virtual environment:
```bash
$ python3 -m venv <env_directory> python=3.8
```

Activate the environment:
```bash
$ source <env_directory>/bin/activate
```

Install library (and their dependencies) as reference from the project directory:
```bash
$ python setup.py develop
```
