import json


condition_dict = {"Tyydyttävä": 3, "Hyvä": 4, "Erinomainen": 5}


class Criteria:

    def __init__(self, price, districts, size):
        self.max_price = int(price)
        self.districts = districts
        self.size = int(size)

        self.number_of_pages = int(0)
        self.number_of_apartments = int(0)
        self.balcony = str()
        self.floor = int()

        self.condition = str()
        self.year_built = int()


    def return_max_price(self):
        return self.max_price

    def return_districts(self):
        return self.districts

    def return_size(self):
        return self.size

    def return_num_of_apartments(self):
        return self.number_of_apartments

    def return_num_of_pages(self):
        return self.number_of_pages

    def return_balcony(self):
        return self.balcony

    def return_floor(self):
        return self.floor

    def return_condition(self):
        return self.condition

    def return_year_built(self):
        return self.year_built


    def how_many_apartments(self, data):
        self.number_of_apartments = data['found'] #update the number of apartments

    def how_many_pages(self):
        if (self.number_of_apartments % 24) == 0:
            self.number_of_pages = self.number_of_apartments / 24
        self.number_of_pages = (self.number_of_apartments // 24) + 1 #update the number of pages

    def check_floor_number_requirement(self, data, i):
        for k, j in enumerate(data):
            content = j.get_text()
            if content == "Kerros":
                if k < len(data) - 1:
                    floor = int(data[k + 1].get_text()[0])
                    if floor >= self.floor:
                        return True
                    return False
         #return boolean based on if the floor number requirement is fulfilled

    def check_balcony_requirement(self, data, i):
        if self.balcony.lower() == "no":
            return True
        for k, j in enumerate(data):
            content = j.get_text()
            if content == "Parveke":
                if k < len(data) - 1:
                    balcony_exists = data[k + 1].get_text()
                    if balcony_exists == "Kyllä" and self.balcony.lower() == "yes":
                        return True
                    return False
         #check if the apartment has a balcony (if user wants it) and return boolean based on the result

    def check_condition_requirement(self, data, i):
        condition_as_integer = condition_dict[self.condition]
        for k, j in enumerate(data):
            content = j.get_text()
            if content == "Kunto":
                if k < len(data) - 1:
                    apartment_condition = condition_dict[data[k + 1].get_text()]
                    if apartment_condition >= condition_as_integer:
                        return True
                    return False
         #check if the apartment fulfills user's condition requirement, if the page doesn't tell the condition, assume it's not ok

    def check_year_requirement(self, data, i):
        for k, j in enumerate(data):
            content = j.get_text()
            if content == "Rakennusvuosi":
                if k < len(data) - 1:
                    year_built = int(data[k + 1].get_text())
                    if year_built >= self.year_built:
                        return True
                    return False
         #check if the apartment fulfills user's year requirement, if the page doesn't tell the condition, assume it's not ok
