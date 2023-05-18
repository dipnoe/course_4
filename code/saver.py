import json
from abc import ABC, abstractmethod

from vacancy import Vacancy


class Saver(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    @abstractmethod
    def add_vacancies_to_json(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass


class JSONSaver(Saver):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """
    JSON_FILE = 'vacancies.json'

    def add_vacancies_to_json(self, vacancies: list):
        with open(self.JSON_FILE, 'w+', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False)

    @property
    def data(self):
        with open(self.JSON_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def json_to_vacancy_class(self):
        vacancies = []
        for i in self.data:
            vacancies.append(Vacancy(i['name'],
                                     i['area'],
                                     i['salary_from'],
                                     i['salary_to'],
                                     i['currency'],
                                     i['experience'],
                                     i['url']))
        return vacancies

    def __get_vacancies_by_criterion(self, criterion: str, value):
        result = []
        for i in self.data:
            if i[criterion] == value:
                result.append(Vacancy(i['name'],
                                      i['area'],
                                      i['salary_from'],
                                      i['salary_to'],
                                      i['currency'],
                                      i['experience'],
                                      i['url']))
        return result

    def get_vacancies_by_min_salary(self, value: int):
        """
        Фильтрация запроса по минимальной зарплате
        """
        return self.__get_vacancies_by_criterion('salary_from', int(value))

    def get_vacancies_by_max_salary(self, value: int):
        """
        Фильтрация запроса по максимальной зарплате
        """
        return self.__get_vacancies_by_criterion('salary_to', int(value))

    def get_vacancies_by_area(self, value):
        """
        Фильтрация запроса по городу
        """
        return self.__get_vacancies_by_criterion('area', value)

    def get_vacancies_by_experience(self, value):
        """
        Фильтрация запроса по опыту работы
        """
        return self.__get_vacancies_by_criterion('experience', value)

    def get_vacancies_by_name(self, value):
        """
        Фильтрация запроса по названию вакансии
        """
        return self.__get_vacancies_by_criterion('name', value)

    def sort_vacancies_by_max_salary(self, number):
        """
        Сортировка вакансий по максимальной зарплате (от большего к меньшему)
        """
        vacancies = self.json_to_vacancy_class()
        vacancies = sorted(vacancies, reverse=True)
        return vacancies[:number]

    def delete_vacancy(self, vacancy: Vacancy):
        for idx, vacancy_dict in enumerate(self.data):
            if vacancy_dict['url'] == vacancy.url:
                self.data.pop(idx)
                break
        self.add_vacancies_to_json(self.data)
