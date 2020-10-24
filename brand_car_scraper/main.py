import requests
from bs4 import BeautifulSoup
import time

def car_scraper(output_file, fp, tp, region):
    milanuncios_scraper = Milanuncios_Scraper();
    milanuncios_scraper.scrap(output_file, fp, tp, region)

#   The URL to obtain data from is: https://www.milanuncios.com/anuncios-en-{province}/?orden=date&fromSearch={page}
#   
#   Where:
#   
#   - province is a string validated by the function validate_region()
#   - page is the number of page result to be requested
#
#
#

class Milanuncios_Scraper:

    def __init__(self):
        self.url = "https://www.milanuncios.com/anuncios-en-"
        self.response_delay = 0.5

    def scrap(self, output_file, fp, tp, region):
        print("region is valid? " + str(self._validate_region(region)) )
        print(f"car_scraper(output_file{output_file!r}, fp={fp!r}, tp={tp!r})")

        for i in range(fp,tp):
            print("Requesting page number " +  str(i))

            initial_time = time.time();
            
            page_content = self._request_page_content(region, i)
            
            self.response_delay = time.time() - initial_time

            cars = self._extract_cars_data(page_content)

            print("the delay was " + str(self.response_delay))

            time.sleep(10 * self.response_delay)

    def _validate_region(self, region):
        return region.lower() in self.regions

    def _request_page_content(self, region, page_number):
        url_to_request = self.url + region.lower() + "/?orden=date&fromSearch="+str(page_number)
        response = requests.get(url_to_request + str(page_number))
        print(response.content)
        return response.content

    def _extract_cars_data(self, page_content):
    #       TODO: Extract data. All the cars are within $('.ma-AdList')
    # 
    #       And, for each car:
    #       
    #           - container:  $('.ma-AdCard-detail').textContent
    #           - model: $('h3.ma-AdCard-bodyTitle') --> {BRAND} - {MODEL}
    #           - photo: $('.ma-AdCard-photoContainer .ma-AdCard-photo').src
    #           - price: $('.ma-AdCard-metadataActions .ma-AdCard-price').textContent
    #           - price currency: $('.ma-AdCard-metadataActions .ma-AdCard-currency').textContent
    #           - seller type: $('.ma-AdCard-metadataTag.ma-AdCard-metadataTag--sellerType .ma-AdTag-label')
    #           - km: $('.ma-AdTagList-item .ma-AdTag-label)[0].textContent 
    #           - year: $('.ma-AdTagList-item .ma-AdTag-label)[1].textContent 
    #           - type of transmission: $('.ma-AdTagList-item .ma-AdTag-label)[2].textContent 
    #           - doors : $('.ma-AdTagList-item .ma-AdTag-label)[3].textContent 
    #           - power : $('.ma-AdTagList-item .ma-AdTag-label)[4].textContent 
    # 
    #
    #
        return None

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