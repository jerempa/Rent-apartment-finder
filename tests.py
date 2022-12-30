import unittest
from input_validation import ErrorHandling
from criteria import Criteria
from url_compiler import Compiler
from file_operations import FileOperations
import string
import random


errorObject = ErrorHandling()

class TestInputValidation(unittest.TestCase):


    def test_return_string_validation(self):
        inputs = [5, "00100, string", "string", "01000"]
        for i in inputs:
            with self.assertRaises(ValueError):
                errorObject.validate_string_input(i) #incorrect inputs
        self.assertEqual(True, errorObject.validate_string_input("00100, 00120, 00900"), "The function should return True!")


random_rent = random.randint(500, 5000)
random_size = random.randint(15, 500)
districts = "00100, 00500, 00800"
criteriaObject = Criteria(random_rent, districts , random_size)

random_num_of_pages = random.randint(0, 10)
random_num_of_apartments = random.randint(0, 500)
random_floor_number = random.randint(1, 20)
random_year_built = random.randint(1500, 2022)

random_balcony_answer = random.choice(["Yes", "No"])
random_condition_answer = random.choice(["Tyydyttävä", "Hyvä", "Erinomainen"])

criteriaObject.number_of_pages = random_num_of_pages
criteriaObject.number_of_apartments = random_num_of_apartments
criteriaObject.balcony = random_balcony_answer
criteriaObject.floor = random_floor_number

criteriaObject.condition = random_condition_answer
criteriaObject.year_built = random_year_built

class TestCriteria(unittest.TestCase):

    def test_return_price(self):
        self.assertEqual(random_rent, criteriaObject.return_max_price(), f"The return value should be {random_rent}")

    def test_return_districts(self):
        self.assertEqual(districts, criteriaObject.return_districts(), f"The return value should be {districts}")

    def test_return_size(self):
        self.assertEqual(random_size, criteriaObject.return_size(), f"The return value should be {random_size}")

    def test_return_num_of_pages(self):
        self.assertEqual(random_num_of_pages, criteriaObject.return_num_of_pages(), f"The return value should be {random_num_of_pages}")

    def test_num_of_apartments(self):
        self.assertEqual(random_num_of_apartments, criteriaObject.return_num_of_apartments(), f"The return value should be {random_num_of_apartments}")
    def test_return_floor_number(self):
        self.assertEqual(random_floor_number, criteriaObject.return_floor(), f"The return value should be {random_floor_number}")

    def test_return_year_built(self):
        self.assertEqual(random_year_built, criteriaObject.return_year_built(), f"The return value should be {random_year_built}")

    def test_balcony_answer(self):
        self.assertEqual(random_balcony_answer, criteriaObject.return_balcony(), f"The return value should be {random_balcony_answer}")

    def test_condition_answer(self):
        self.assertEqual(random_condition_answer, criteriaObject.return_condition(), f"The return value should be {random_condition_answer}")

compilerObject = Compiler()
random_url = ''.join(random.choice(string.ascii_lowercase) for i in range(50))

class TestURLCompiling(unittest.TestCase):

    def test_return_url(self):
        compilerObject.url = random_url
        self.assertEqual(random_url, compilerObject.return_url(), f"The return value should be {random_url}!")


fileoperationObject = FileOperations()
random_ids_list = [random.randint(1,100) for _ in range(25)]

class TestFileOperations(unittest.TestCase):

    def test_return_apartment_ids(self):
        fileoperationObject.apartment_ids = random_ids_list
        self.assertEqual(random_ids_list, fileoperationObject.return_apartment_ids(), f"The return value should be {random_ids_list}!")

if __name__ == '__main__':
    unittest.main()