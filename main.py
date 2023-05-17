from api import HeadHunterAPI, SuperJobAPI
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

if __name__ == "__main__":
    user_interaction()
