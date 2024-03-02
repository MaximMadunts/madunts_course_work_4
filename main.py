from src.classes import HeadHunterAPI, Connector, Vacancy
from tabulate import tabulate
import pandas as pd
import os
import json


def main():
    # keyword = "Python"
    keyword = input("Введите ключевое слово вакансии: ")

    """Создание экземпляров класса для работы с API сайта с вакансиями"""
    hh = HeadHunterAPI()
    path = 'data/vacancies.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as json_file:
            vacs = json.load(json_file)
            connector = Connector(keyword=keyword, vacancies_list=vacs)
    else:
        vacs = hh.get_vacancies()
        connector = Connector(keyword=keyword, vacancies_list=vacs)
        connector.insert()

    while True:
        command = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате;\n"
            "exit - для выхода.\n"
            ">>> "
        )
        print(command)
        if command.lower() == "exit":
            break
        elif command == '1':
            vacancies = connector.select()
            df = pd.DataFrame(vacancies)
            df = tabulate(df, headers=['Компания', 'Должность', 'Ссылка на вакансию', 'ЗП от', 'ЗП до', 'Валюта',
                                       'Город'])
            print(df)
        elif command == '2':
            connector.sorted_by_salary()




if __name__ == "__main__":
    main()
