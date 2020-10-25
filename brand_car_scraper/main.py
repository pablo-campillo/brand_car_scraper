from bs4 import BeautifulSoup
import time
import pandas as pd
import click

from pyvirtualdisplay import Display
from selenium import webdriver
from uuid import uuid4
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def car_scraper(output_file, fp, tp, region):
    milanuncios_scraper = MilanunciosScraper()
    milanuncios_scraper.scrap(output_file, fp, tp, region)


class MilanunciosScraper:
    """ Class to scrap vehicle ads from https://www.milanuncios.com/coches-de-segunda-mano-en-{province}/?fromSearch={page}&orden=date
    Where:
        - province is a string validated by the function validate_region()
        - page is the number of page result to be requested
    """

    DELAY_RATIO = 10 # Number of times that it waits depending on the response time for the next requests

    def __init__(self, executable_path = "brand_car_scraper/chromedriver", log_path="chromedriver.log"):
        self._response_delay = 0.5
        self._executable_path = executable_path

    def scrap(self, output_file, fp, tp, region):
        fp = 1 if not fp else fp
        tp = 1 if not tp else tp # TODO if tp is None tp should be equal to total number of pages

        self._start_session()

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

        dataset.to_csv(output_file)

    def _validate_region(self, region):
        return region.lower() in self.regions

    def _start_session(self):
        """Internal function to start a virtual session"""
        self.session = uuid4()
        click.secho(f"Starting chrome session", fg='green')

        display = Display(visible=1, size=(1024, 768))
        display.start()

        self.browser = webdriver.Chrome(self._executable_path)

        self.browser.get("https://www.milanuncios.com/coches-de-segunda-mano-en-{region}/")

        time.sleep(10)


    def _request_page_content(self, region, page_number):
        url = f"https://www.milanuncios.com/coches-de-segunda-mano-en-{region}/?fromSearch={page_number}&orden=date"
        
        initial_time = time.time()

        response = self.browser.get(url)

        self.browser.find_element_by_tag_name('body').send_keys(Keys.END)            
        
        self.response_delay = time.time() - initial_time

        time.sleep(self.DELAY_RATIO * self._response_delay)

        click.secho(f"The delay was {self._response_delay}")

        return self.browser.page_source

    def _obtain_cookies(self):
        return {c['name']:c['value'] for c in self._cookies}


    def _extract_all_cars_data(self, page_content: str) -> list:
        """Parses the page_content and returns a list of dict with car features

        :param page_content: string with html content
        :return: ditc with f
        """
        result = []
        soup = BeautifulSoup(page_content, 'html.parser')
        
        
        articles = soup.find_all('article', 'ma-AdCard')
        
        for article in articles:
            car_record = self._extract_cars_record(article)
            result.append(car_record)
        

        return result

    def _extract_cars_record(self, article) -> dict:
        ad_type = self._get_text(article, 'p', 'ma-AdCard-sellType', default=None)

        if ad_type.upper() != "OFERTA":
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