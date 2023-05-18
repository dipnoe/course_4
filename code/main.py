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

        # Получение вакансий с разных платформ по ключевому слову
        for api in (hh_api, superjob_api):
            api.get_vacancies(keyword_search)
            vacancies.extend(api.get_formatted_vacancies())

        # Сохранение информации о вакансиях в файл и преобразование экземпляров в класс Vacancy
        json_saver = JSONSaver(keyword_search)
        json_saver.add_vacancies_to_json(vacancies)
        vacancies_json = json_saver.json_to_vacancy_class()

        show_user = input("Вывести весь список? (1 - да, 2 - фильтровать)\n>>> ")
        if show_user == '1':
            for vacancy in vacancies_json:
                print(vacancy)

        if show_user == '2':
            filter_word = input("""Выберите фильтр:
1 - По минимальной зарплате
2 - По максимальной зарплате
3 - По городу
4 - По опыту(Возможные значения: 1 — без опыта, 2 — от 1 года, 3 — от 3 лет, 4 — от 6 лет)
5 - Вывести топ вакансий по зарплате\n>>> """)

            filtered_vacancies = ''

            if filter_word == '5':
                top_n = input("Введите количество вакансий для топа:\n>>> ")
                if top_n.isdigit():
                    filtered_vacancies = json_saver.sort_vacancies_by_max_salary(int(top_n))
                    for i in filtered_vacancies:
                        print(i)

            elif filter_word in ('1', '2', '3', '4'):
                input_value = input("Введите значение:\n>>> ").lower()

                if filter_word == '1':
                    filtered_vacancies = json_saver.get_vacancies_by_min_salary(int(input_value))
                    for i in filtered_vacancies:
                        print(i)

                if filter_word == '2':
                    filtered_vacancies = json_saver.get_vacancies_by_max_salary(int(input_value))
                    for i in filtered_vacancies:
                        print(i)

                if filter_word == '3':
                    filtered_vacancies = json_saver.get_vacancies_by_area(input_value)
                    for i in filtered_vacancies:
                        print(i)

                if filter_word == '4':
                    experience = {'1': 'Без опыта',
                                  '2': 'От 1 года',
                                  '3': 'От 3 лет',
                                  '4': 'От 6 лет'
                                  }
                    filtered_vacancies = json_saver.get_vacancies_by_experience(experience[input_value])
                    for i in filtered_vacancies:
                        print(i)

            else:
                print('Некорректное значение')

            user_save = input("Сохранить результаты в файл?(1 - да, 0 - выход)")
            if user_save == '1':
                json_saver.add_vacancies_to_json(filtered_vacancies)
            elif user_save == '0':
                break


if __name__ == "__main__":
    user_interaction()
