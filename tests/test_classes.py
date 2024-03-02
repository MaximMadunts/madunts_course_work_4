import unittest
from unittest.mock import patch

from src.classes import Connector


class TestHeadHunterAPI(unittest.TestCase):

    def test_get_request(self):
        # тест для метода get_request
        pass

    def test_get_formatted_vacancies(self):
        # тест для метода get_formatted_vacancies
        pass

    def test_get_vacancies(self):
        #  тест для метода get_vacancies
        pass


class TestVacancy(unittest.TestCase):

    def test_ge_method(self):
        #  тест для метода __ge__
        pass

    def test_le_method(self):
        #  тест для метода __le__
        pass


class TestConnector(unittest.TestCase):

    def setUp(self):
        # Подготовка данных для тестирования
        self.vacancies_list = [
            {"title": "Python Developer", "salary_from": 50000, "salary_to": 80000},
            {"title": "Java Developer", "salary_from": 60000, "salary_to": 90000},
            # Другие вакансии
        ]
        self.keyword = "Python"
        self.connector = Connector(self.vacancies_list, self.keyword)

    def test_insert(self):
        # тест для метода insert
        pass

    def test_select(self):
        # тест для метода select
        pass

    def test_sorted_by_salary(self):
        # тест для метода sorted_by_salary
        pass

    def test_delete(self):
        # тест для метода delete
        pass


if __name__ == '__main__':
    unittest.main()
