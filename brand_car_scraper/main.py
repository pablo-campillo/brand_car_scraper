from bs4 import BeautifulSoup
import time
import pandas as pd
import click

from uuid import uuid4
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pathlib import Path


def car_scraper(output_file, fp, tp, region):
    milanuncios_scraper = MilanunciosScraper()
    milanuncios_scraper.scrap(output_file, fp, tp, region)


class MilanunciosScraper:
    """ Class to scrap vehicle ads from https://www.milanuncios.com/coches-de-segunda-mano-en-{region}/?fromSearch={page}&orden=date
    Where:
        - region is a string validated by the function validate_region()
        - page is the number of page result to be requested
    """

    def __init__(self, executable_path="brand_car_scraper/chromedriver", log_path="chromedriver.log"):
        self._response_delay = 0.5
        self._executable_path = executable_path

    def scrap(self, output_file, fp, tp, region):
        output_file_path = Path(output_file)

        self.current_page = 1 if not fp else fp
        self.max_page = tp

        if not self._validate_region(region):
            click.secho(f"Not valid region name error: {region}", fg='red')
            click.secho(f"Valid region names: {self.regions}", fg='red')
            return

        dataset = pd.DataFrame()

        while True:
            try:
                self.parse_pages(dataset, output_file_path, region)
                break
            except TimeoutException as e:
                click.secho(f"Browser Timeout Exception!", fg="red")
                continue

    def parse_pages(self, dataset, output_file_path, region):
        with SeleniumBrowser() as sb:
            must_add_headers = True

            for page_number in self._pages_to_scrap():
                click.echo(page_number)
                page_content = sb.read(self._get_url(region, page_number))

                if page_content:
                    parser = MilAnunciosPageParser(page_content)
                    self._update_max_page(parser)

                    records = parser.get_records()
                    if len(records) > 0:
                        df = pd.DataFrame(records)
                        df['region'] = region
                        df.to_csv(output_file_path.parent / f"{output_file_path.name}", mode="a", header = must_add_headers)
                        dataset = pd.concat([dataset, pd.DataFrame(records)])
                        dataset['region'] = region
                        
                        if must_add_headers: must_add_headers = False

    def _get_url(self, region, page_number):
        return f"https://www.milanuncios.com/coches-de-segunda-mano-en-{region}/?pagina={page_number}&orden=date"

    def _pages_to_scrap(self):
        while True:
            if self.max_page and self.current_page > self.max_page:
                break
            yield self.current_page
            self.current_page += 1

    def _update_max_page(self, page_parser):
        if not self.max_page and page_parser:
            self.max_page = page_parser.get_total_number_of_pages()
            click.secho(f"Number of pages: {self.max_page}", fg="green")

    def _validate_region(self, region):
        return region.lower() in self.regions

    @property
    def regions(self):
        return [
            'alava', 'albacete', 'alicante', 'almeria', 'aragon',
            'asturias', 'avila', 'badajoz', 'baleares', 'barcelona', 'burgos',
            'caceres', 'cadiz', 'cantabria', 'castellon','ceuta','ciudad_real',
            'cordoba', 'cuenca','girona', 'granada', 'guadalajara', 'guipuzcoa', 
            'huelva', 'huesca', 'jaen', 'la_coruna', 'la_rioja', 'las_palmas', 'leon',
            'lleida', 'lugo', 'madrid', 'malaga', 'melilla', 'murcia', 'navarra',
            'ourense', 'palencia', 'pontevedra', 'salamanca', 'segovia', 'sevilla',
            'soria', 'tarragona', 'tenerife', 'teruel', 'toledo', 'valencia',
            'valladolid', 'vizcaya','zamora', 'zaragoza'
        ]


class MilAnunciosPageParser:
    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')

    def get_records(self):
        return self._extract_all_cars_data(self.soup.find_all('article', {'class': 'ma-AdCard'}))

    def get_total_number_of_pages(self):
        result = None
        div = self.soup.find('div', 'ma-NavigationPagination-pagesContainer')
        if div:
            pages = div.find_all('span', 'ma-ButtonBasic-content')
            if pages:
                result = int(pages[-1].text)
                click.secho(f"Total number of paged found: {result}", fg='green')
        return result

    def _extract_all_cars_data(self, articles: list) -> list:
        result = []
        for article in articles:
            car_record = self._extract_cars_record(article)
            if car_record is None:
                continue
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

        fields = [p.text for p in article.find('ul', 'ma-AdTagList').find_all('span', 'ma-AdTag-label')]
        if len(fields) != 5:
            return None
        car_km, car_year, car_engine_type, car_door_num, car_power = fields

        price_section = article.find('div', 'ma-AdCard-metadataActions')
        car_price = self._get_text(price_section, 'span', 'ma-AdCard-price', default=None)
        if car_price:
            car_price = car_price.replace('.', '').replace('€', '')
        advertizer_type = self._get_text(price_section, 'span', 'ma-AdTag-label', default=None)

        image_url = article.find('img', 'ma-AdCard-photo').get('src') if article.find('img', 'ma-AdCard-photo') else ""

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


class SeleniumBrowser:
    MAX_SCROLLS = 100

    def __init__(self, load_page_timeout=5, scroll_pause_time=1):
        self.load_page_timeout = load_page_timeout
        self.scroll_pause_time = scroll_pause_time

    def __enter__(self):
        self.session = uuid4()
        click.secho(f"Starting chrome session", fg='green')

        options = Options()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')

        self.browser = webdriver.Chrome(executable_path="brand_car_scraper/chromedriver", chrome_options=options)
        return self

    def __exit__(self, type, value, traceback):
        click.secho(f"Closing chrome session", fg='green')
        self.browser.quit()

    def read(self, url):

        self.browser.get(url)
        try:
            WebDriverWait(self.browser, self.load_page_timeout).until(lambda d: d.find_element_by_tag_name("article"))
        except TimeoutException:
            click.secho(f"Timed out waiting for page to load: {url}", fg="red")
            return None

        scroll_counter = 1
        while scroll_counter < self.MAX_SCROLLS:
            ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(self.scroll_pause_time)
            self._accept_cookies()
            try:
                next_page_element = self.browser.find_element_by_class_name("ma-NavigationPagination-nextButton")
                break
            except:
                continue

        return self.browser.page_source

    def _accept_cookies(self):
        try:
            buttons = self.browser.find_elements_by_class_name("sui-AtomButton--primary")
        except:
            return
        if buttons:
            buttons[0].click()