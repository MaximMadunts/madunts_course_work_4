import json
import os
import random
import time
from abc import ABC, abstractmethod
from configparser import ParsingError

import requests
from pydash import get


class ArcConnector(ABC):
    """Абстрактный родительский класс"""

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def sorted_by_salary(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class Engine(ABC):
    """Абстрактный родительский класс"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass


class HeadHunterAPI(Engine):

    def __init__(self):

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Cookie': 'hhtoken=SgrlbHpPwXasO17_B38Vm1tgyUGt; hhuid=q9OKf2FoOGIzXmPD0KgyCw--; _ga=GA1.2.466181570.1673777324; _ga_44H5WGZ123=GS1.1.d552011a6f446deffc60438eda4e1d6486fbc35788baa01ae0bcc39182ddec7b.46.1.1678434110.60.0.0; hhul=e962eaedfb678fa1d5c142826c3ef21d5de6472513210c9a1d0840838751817f; cookie_policy_agreement=true; __zzatgib-w-hh=MDA0dC0jViV+FmELHw4/aQsbSl1pCENQGC9LX3svOx8gaEoVJ3gPTX5bTxY1JCkNCRRiQnYpeDA+Z1AZOVURCxIXRF5cVWl1FRpLSiVueCplJS0xViR8SylEXE18Jx0TfG8nVQ4RVy8NPjteLW8PKhMjZHYhP04hC00+KlwVNk0mbjN3RhsJHlksfEspNRJ+CixOQjFzJwl/DhlDSHF4XEIhHhl5WSZLDn8JKk5CeHQrCQwLGUYzaWVpcC9gIBIlEU1HGEVkW0I2KBVLcU8cenZffSpCZSBhS1skR1lTCCYVe0M8YwxxFU11cjgzGxBhDyMOGFgJDA0yaFF7CT4VHThHKHIzd2UtPmUjaEhcJDVRP0FaW1Q4NmdBEXUmCQg3LGBwVxlRExpceEdXeiwZFHlvJVQLD2FERWllbQwtUlFRS2IPHxo0aQteTA==a2Nhhg==; gsscgib-w-hh=VsOXs5CDk0cZAEmLr9aJQkM9gagskovvMWTXzBmJSHJvDthf+ojuyurpA/EowdpFfyXV9OgYfA/mFUmuGGJBETVxxx+6g4Vk/auN/S3DCoTaOB00ywwpUnEsbIZ5PkiFopVL66t7tQ8p3BBDxw0KvL5Wo3T5fACMVa90FOvVqwidil2hUv5Un/XthXcG1QUA4nfaqTUMjY62CjVSgMgYPbwSZUU+90C1u/I3jXUsemzKTVXNYCq2j01+v0Vkx7WBiq0=; fgsscgib-w-hh=KMsp09dd9bdb5ca38cdba5b2f3c24b01433547f7; cfidsgib-w-hh=GFrmR8FvoNOVBx7sTMpOFrHzWW0O8yCVzVEsSaH5XXLI3/pua+rxOhNnKSBykdMLF1hXWIK5UB3oT/lUCUtD5M92QqQULWrYtgYO1QzK4WupDGcqeoC+/dV+XgB+NQy8q5+VdKF4Ila7Hu1ZQB5ey/2JYvjKXIrfOpwivYZq; __ddg1_=smIJLZa24J0BGnDToMrZ',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

    def get_request(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус: {response.status_code}')
        res = response.json()
        return res['items']

    def get_formatted_vacancies(self, url):
        formatted_vacancies = []
        for vacancy in self.get_request(url):
            formatted_vacancy = {
                "employer": get(vacancy, "employer.name"),
                "title": get(vacancy, "name"),
                "url": get(vacancy, "alternate_url"),
                "salary_from": get(vacancy, "salary.from"),
                "salary_to": get(vacancy, "salary.to"),
                "currency": get(vacancy, "salary.currency"),
                "country": get(vacancy, "area.name")
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

    def get_vacancies(self, pages_count=19):
        vacancies = []
        r = random.randint(1, 2)
        time.sleep(r)
        for page in range(1, pages_count):
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            url = f"https://api.hh.ru/vacancies/?per_page=100&page={page}"
            try:
                page_vacancies = self.get_formatted_vacancies(url)
                vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(vacancies)}")
            except ParsingError as error:
                print(error)

        return vacancies


class Vacancy:
    def __init__(self, employer, title, url, salary_from, salary_to, currency, country):
        self.employer = employer  # работодатель
        self.title = title  # вакансия
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.country = country

    def __str__(self):

        return f"Работодатель: {self.employer}\n" \
               f"Вакансия: {self.title}\n" \
               f"Зарплата: от {self.salary_from} до {self.salary_to}\n" \
               f"Ссылка: {self.url}\n" \
               f"Город: {self.country}\n" \
               f"Валюта: {self.currency}\n"

    def __ge__(self, other):
        if self.salary_from is not None and other.salary_to is not None:
            return self.salary_from >= other.salary_to
        else:
            print("ЗП не указана")

    def __le__(self, other):
        if self.salary_from is not None and other.salary_to is not None:
            return self.salary_from <= other.salary_to
        else:
            print("ЗП не указана")


class Connector(ArcConnector):
    def __init__(self, vacancies_list, keyword):
        self.keyword = keyword
        self.vacancies_list = vacancies_list

    def insert(self):
        f = json.dumps(self.vacancies_list, ensure_ascii=False, indent=4)
        with open('data/vacancies.json', 'w', encoding='utf-8') as json_file:
            json_file.write(f)

    def select(self):
        selected_vacs = []
        for i in self.vacancies_list:
            if self.keyword in i['title']:
                selected_vacs.append(i)
        return selected_vacs

    def sorted_by_salary(self):
        return [print(Vacancy(**x)) for x in self.select()]

    def delete(self):
        os.remove(self.filename)
