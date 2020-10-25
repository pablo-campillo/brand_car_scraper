import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import click
from datetime import datetime


def car_scraper(output_file, fp, tp, region):
    milanuncios_scraper = MilanunciosScraper()
    milanuncios_scraper.scrap(output_file, fp, tp, region)


class MilanunciosScraper:
    """ Class to scrap vehicle ads from https://www.milanuncios.com/coches-de-segunda-mano-en-{province}/?fromSearch={page}&orden=date
    Where:
        - province is a string validated by the function validate_region()
        - page is the number of page result to be requested
    """

    RETRAY_NUMBER = 5 # if no page content is gather it request the same page again until retay_number times
    DELAY_RATIO = 10 # Number of times that it waits depending on the response time for the next requests

    def __init__(self):
        self.response_delay = 0.5

    def scrap(self, output_file, fp, tp, region):
        fp = 1 if not fp else fp
        tp = 1 if not tp else tp # TODO if tp is None tp should be equal to total number of pages
        if not self._validate_region(region):
            click.secho(f"Not valid region name error: {region}", fg='red')
            click.secho(f"Valid region names: {self.regions}", fg='red')
            return

        dataset = pd.DataFrame()
        for page_number in range(fp, tp+1): # TODO generator that return the next page number depending on fp and tp
            page_content = self._request_page_content(region, page_number)

            if page_content:
                cars = self._extract_all_cars_data(page_content)
                dataset = pd.concat([dataset, pd.DataFrame(cars)])
                dataset['region'] = region

            time.sleep(self.DELAY_RATIO * self.response_delay)

        dataset.to_csv(output_file)

    def _validate_region(self, region):
        return region.lower() in self.regions

    def _request_page_content(self, region, page_number):
        url = f"https://www.milanuncios.com/coches-de-segunda-mano-en-{region}/?fromSearch={page_number}&orden=date"

        req_counter = 1
        page_content = None
        while not page_content and req_counter <= self.RETRAY_NUMBER:
            click.secho(f"Requesting page number {page_number}, try #{req_counter}", fg='green' if req_counter == 1 else 'orange')
            initial_time = time.time();
            response = requests.get(url)
            self.response_delay = time.time() - initial_time
            click.secho(f"The delay was {self.response_delay}")
            page_content = response.content if response.status_code == 200 else None
            req_counter += 1
        return page_content

    def _extract_all_cars_data(self, page_content: str) -> list:
        """Parses the page_content and returns a list of dict with car features

        :param page_content: string with html content
        :return: ditc with f
        """
        result = []
        soup = BeautifulSoup(page_content, 'html.parser')
        # TODO iterate over all articles
        article = soup.find('article', 'ma-AdCard')
        car_record = self._extract_cars_record(article)
        result.append(car_record)
        
        return result

    def _extract_cars_record(self, article) -> dict:
        ad_type = self._get_text(article, 'p', 'ma-AdCard-sellType', default=None)

        if ad_type != "OFERTA":
            return None

        ad_id = self._get_text(article, 'p', 'ma-AdCard-adId', default=None)
        ad_time = self._get_text(article, 'p', 'ma-AdCard-time', default=None)

        ad_title = self._get_text(article, 'h3', 'ma-AdCard-bodyTitle', default=None)
        car_desc = self._get_text(article, 'p', 'ma-AdCard-text', default=None)

        car_km, car_year, car_engine_type, car_door_num, car_power = [
            p.text for p in article.find('ul', 'ma-AdTagList').find_all('span','ma-AdTag-label')]

        price_section = article.find('div', 'ma-AdCard-metadataActions')
        car_price = self._get_text(price_section, 'span', 'ma-AdCard-price', default=None)
        if car_price:
            car_price = car_price.replace('.', '').replace('€', '')
        advertizer_type = self._get_text(price_section, 'span', 'ma-AdTag-label', default=None)

        image_url = article.find('img', 'ma-AdCard-photo').get('src')

        return {
            'ad_id': ad_id,
            'ad_type': ad_type,
            'ad_time': ad_time,
            'ad_title': ad_title,
            'car_desc': car_desc,
            'car_km': car_km,
            'car_year': car_year,
            'car_engine_type': car_engine_type,
            'car_door_num': car_engine_type,
            'car_power': car_power,
            'car_price': car_price,
            'advertizer_type': advertizer_type,
            'image_url': image_url,
            'ts': datetime.utcnow(),
        }

    def _get_text(self, article, name, attrs, default=None):
        result = article.find(name, attrs)
        return result.text if result else default

    @property
    def regions(self):
        return [
            'alava', 'albacete', 'alicante', 'almeria', 'andalucia', 'aragon',
            'asturias', 'avila', 'badajoz', 'baleares', 'barcelona', 'burgos',
            'caceres', 'cadiz', 'cantabria', 'canarias', 'castellon',
            'castilla_la_mancha', 'castilla_y_leon', 'catalunya', 'ceuta',
            'ciudad_real', 'cordoba', 'cuenca', 'extremadura', 'galicia',
            'girona', 'granada', 'guadalajara', 'guipuzcoa', 'huelva',
            'huesca', 'jaen', 'la_coruna', 'la_rioja', 'las_palmas', 'leon',
            'lleida', 'lugo', 'madrid', 'malaga', 'melilla', 'murcia', 'navarra',
            'ourense', 'pais_vasco', 'palencia', 'pontevedra', 'salamanca',
            'segovia', 'sevilla', 'soria', 'tarragona', 'tenerife', 'teruel',
            'toledo', 'valencia', 'comunidad_valenciana', 'valladolid', 'vizcaya',
            'zamora', 'zaragoza'
        ]        