import json
from abc import ABC, abstractmethod

from vacancy import Vacancy


class Saver(ABC):
    """
    Определить абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
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