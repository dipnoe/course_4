from code.api import HeadHunterAPI, SuperJobAPI
from saver import JSONSaver


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()


# # Функция для взаимодействия с пользователем
def user_interaction():
    vacancies = []
    while True:

        keyword_search = input("Введите вакансию для поиска (0 - выход)\n>>> ")
        if keyword_search == '0':
            break

        for api in (hh_api, superjob_api):
            api.get_vacancies(keyword_search)
            vacancies.extend(api.get_formatted_vacancies())

        # Сохранение информации о вакансиях в файл и преобразование экземпляров в класс Vacancy
        json_saver = JSONSaver()
        json_saver.add_vacancies_to_json(vacancies)
        vacancies_json = json_saver.json_to_vacancy_class()

        show_user = input("Вывести весь список? (1 - да, 2 - фильтровать)\n>>> ")
        if show_user == '1':
            for vacancy in vacancies_json:
                print(vacancy)

        if show_user == '2':
            filter_word = input("""Выберите фильтр:
1 - по минимальной зарплате
2 - по максимальной зарплате
3 - по городу
4 - по опыту('Возможные значения: 1 — без опыта, 2 — от 1 года, 3 — от 3 лет, 4 — от 6 лет')\n>>> """)

            input_value = input("Введите значение:\n>>> ").lower()
            if filter_word == '1':
                for i in json_saver.get_vacancies_by_min_salary(int(input_value)):
                    print(i)
            elif filter_word == '2':
                for i in json_saver.get_vacancies_by_max_salary(int(input_value)):
                    print(i)
            elif filter_word == '3':
                for i in json_saver.get_vacancies_by_area(input_value):
                    print(i)
            elif filter_word == '4':
                experience = {'1': 'Без опыта',
                              '2': 'От 1 года',
                              '3': 'От 3 лет',
                              '4': 'От 6 лет'
                              }
                for i in json_saver.get_vacancies_by_experience(experience[input_value]):
                    print(i)

            else:
                print('Некорректное значение')


if __name__ == "__main__":
    user_interaction()
