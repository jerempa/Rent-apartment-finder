import json

class FileOperations:

    def __init__(self):
        self.apartment_ids = None
        self.applicable_apartment_urls = None
        self.data = None

    def return_apartment_ids(self):
        return self.apartment_ids

    def return_apartment_urls(self):
        return self.applicable_apartment_urls

    def write_data(self, data):
        self.data = data
        if self.data['start'] == 0:
            f = open("apartment_info.txt", "w")
        else:
            f = open("apartment_info.txt", "a")
        for i in self.data['cards']:
            f.write(json.dumps(i))
            f.write("\n")
        f.close()
        return True #write the data to a file

    def read_data(self):
        f = open("apartment_info.txt", "r")
        list_of_apartment_ids = []
        for line in f:
            line = line.rstrip()
            line = json.loads(line)
            list_of_apartment_ids.append((line['id']))
        f.close()

        self.apartment_ids = list_of_apartment_ids #make a list of apartment ids that are applicable at the moment

    def update_data(self):
        f = open("apartment_info.txt", "r")
        file = open("apartment_info_updated.txt", "w")
        for line in f:
            line = line.rstrip()
            line = json.loads(line)
            if line['id'] in self.apartment_ids:
                file.write(json.dumps(line))
                file.write("\n")
        f.close()
        file.close()

        return True #update the applicable apartments after more parametres

    def parse_apartment_urls(self):
        f = open("apartment_info_updated.txt", "r")
        list_of_apartment_urls = []
        for line in f:
            line = line.rstrip()
            line = json.loads(line)
            list_of_apartment_urls.append((line['url']))
        f.close()

        self.applicable_apartment_urls = list_of_apartment_urls #parse the apartment urls from the information