import requests
from bs4 import BeautifulSoup
import random
import json
import webbrowser
from criteria import Criteria
from url_compiler import Compiler
from file_operations import FileOperations

class Requests:

    def __init__(self, price, districts, size, criteria_object, file_operations_object):
        self.max_price = price
        self.districts = districts
        self.size = size

        self.cookie = str()
        self.ota_token = str()
        self.cuid = str()
        self.loaded = str()

        self.list_of_ids = list()

        self.compiler = Compiler()
        self.fileope = file_operations_object
        self.criteria = criteria_object

        self.num_of_apartments = int(0)
        self.num_of_pages = int(0)

        self.get_ota_token()
        self.districts_as_a_list()
        self.location_query()
        self.get_request_to_server()

        self.loop_through_pages()
        self.applicable_apartments = None


    def return_cookie(self):
        return self.cookie

    def return_ota_token(self):
        return self.ota_token

    def return_cuid(self):
        return self.cuid

    def return_loaded(self):
        return self.loaded

    def return_loop_value(self):
        return self.loop_value

    def get_cookie(self):
        url = "https://asunnot.oikotie.fi/"
        response = requests.get(url)
        headers = response.headers
        self.cookie = headers['Set-cookie'] #get the cookie (isn't necessary)

    def get_ota_token(self):
        random_number = random.randint(0,99999)
        url = "https://asunnot.oikotie.fi/vuokra-asunnot?pagination=1&locations=%5B%5B64,6,%22Helsinki%22%5D%5D&cardType=101"
        response = requests.get(url)
        parser = BeautifulSoup(response.text, 'html.parser')
        token = parser.find('meta', {'name':'api-token'})
        self.ota_token = token['content']

        cuid = parser.find('meta', {'name':'cuid'})
        self.cuid = cuid['content']

        loaded = parser.find('meta', {'name':'loaded'})
        self.loaded = loaded['content']

        #get ota token and other values for authorization

    def get_request_to_server(self):
        price_max = f"&price%5Bmax%5D={self.max_price}&"
        size_min = f"size%5Bmin%5D={self.size}"

        self.compiler.compile_url(self.num_of_pages, self.max_price, self.size, self.list_of_ids, self.districts) #compile the url for the request
        url = self.compiler.return_url()
        headers = {'ota-token': self.ota_token, 'ota-cuid': self.cuid, 'ota-loaded': self.loaded}
        response = requests.get(url, headers=headers)
        data = response.json() #compile url and make a get request to the page

        self.num_of_apartments = int(data['found'])
        self.fileope.write_data(data)

        self.criteria.how_many_apartments(data)
        self.num_of_apartments = self.criteria.return_num_of_apartments()
        self.criteria.how_many_pages()
        self.num_of_pages = self.criteria.return_num_of_pages() #write the data of the first page to a file and update the number of pages and apartments

    def location_query(self):
        headers = {'ota-token': self.ota_token, 'ota-cuid': self.cuid, 'ota-loaded': self.loaded}
        list_of_ids = []

        for i in self.districts:
            url = f"https://asunnot.oikotie.fi/api/3.0/location?query={i}"
            response = requests.get(url, headers=headers)
            data = response.json()
            list_of_ids.append(self.filter_location_id(data))

        self.list_of_ids = list_of_ids #get the ids of the apartments

    def districts_as_a_list(self):
        districts = self.districts
        districts = districts.split(',')
        list_of_districts = []

        for i in districts:
            i = i.lstrip()
            list_of_districts.append(i)

        self.districts = list_of_districts
        #get the districts as a list


    def filter_location_id(self, response):
        location_id = response[0]['card']['cardId']

        return location_id #return the id of a certain district

    def loop_through_pages(self):
        num_of_apartments_per_page = 24

        for i in range(1, self.num_of_pages):
            self.compiler.compile_url(i * num_of_apartments_per_page, self.max_price, self.size, self.list_of_ids, self.districts)
            url = self.compiler.return_url()
            headers = {'ota-token': self.ota_token, 'ota-cuid': self.cuid, 'ota-loaded': self.loaded}
            response = requests.get(url, headers=headers)
            data = response.json()
            self.fileope.write_data(data)

        #loop through the number of pages and make a get request to the page, write data to a file


    def get_requests_to_apartments(self):
        self.fileope.read_data()
        apartment_ids = self.fileope.return_apartment_ids()
        valid_apartments = []

        for index, id in enumerate(apartment_ids):
            self.compiler.compile_apartment_url(id)
            url = self.compiler.return_apartment_url()
            headers = {'ota-token': self.ota_token, 'ota-cuid': self.cuid, 'ota-loaded': self.loaded}
            response = requests.get(url, headers=headers)
            parser = BeautifulSoup(response.text, 'html.parser')
            data = parser.find_all(["dt", "dd"]) #make requests to the apartment pages and parse the text
            yield index #return the index for the progress bar
            if self.criteria.check_year_requirement(data, id):
                if self.criteria.check_balcony_requirement(data, id):
                    if self.criteria.check_floor_number_requirement(data, id):
                        if self.criteria.check_condition_requirement(data, id):
                            valid_apartments.append(id) #check the requirements of the user, start with year as it (most likely) makes the most amount of apartments unapplicable

        self.fileope.apartment_ids = valid_apartments #update the value of applicable apartments

        update_data = self.fileope.update_data()
        if update_data == True:
            urls = self.fileope.parse_apartment_urls()  #write to a file and parse the urls for the user to open



