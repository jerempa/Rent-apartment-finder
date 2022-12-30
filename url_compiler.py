import json


class Compiler:

    def __init__(self):
        self.url = str()
        self.apartment_url = str()

    def return_url(self):
        return self.url

    def return_apartment_url(self):
        return self.apartment_url

    def compile_url(self, page, price, size, location_ids, districts):
        location_string = str("%5B")
        price_max = f"&price%5Bmax%5D={price}&"
        size_min = f"size%5Bmin%5D={size}"
        for i in range(len(location_ids)):
            if (i + 1) == len(location_ids):
                location_string += f"%5B{location_ids[i]},5,%22{districts[i]},+Helsinki%22%5D"
            else:
                location_string += f"%5B{location_ids[i]},5,%22{districts[i]},+Helsinki%22%5D,"

        self.url = f"https://asunnot.oikotie.fi/api/cards?cardType=101&limit=24&locations={location_string}%5D&offset={page}{price_max}{size_min}&sortBy=published_sort_desc" #compile url for the pages that has the apartments

    def compile_apartment_url(self, id):
        self.apartment_url = f"https://asunnot.oikotie.fi/vuokra-asunnot/helsinki/{id}" #compile url for the apartment pages

