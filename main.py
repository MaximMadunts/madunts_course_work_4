from src.classes import HeadHunterAPI, Connector, Vacancy


def main():
    global vacancies
    vacancies_json = []
    keyword = "Python"

    """Создание экземпляров класса для работы с API сайта с вакансиями"""
    hh = HeadHunterAPI(keyword)



    # Сохранение информации о вакансиях в файл
    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json=vacancies_json)
    connector.select(vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате;\n"
            "exit - для выхода.\n"
            ">>> "
        )
        if command.lower() == "exit":
            break
        elif command == "1":
            vacancies = connector.select("Python")
        elif command == "2":
            vacancies = connector.sorted_by_salary()
        for vacancy in vacancies:
            print(vacancy, end="\n")


if __name__ == "__main__":
    main()

