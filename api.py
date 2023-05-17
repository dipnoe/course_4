import os
from abc import ABC, abstractmethod

import requests

from errors import HHResponseError, SJResponseError


class API(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_vacancies(self, vacancy):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API hh.ru
    """

    def __init__(self, area=113):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            'text': None,
            'area': area,
            'page': 1,
            'per_page': 100,
        }
        self.vacancies = []

    def get_response(self):
        response = requests.get(self.url, params=self.params)
        if not response.ok:
            raise HHResponseError
        return response.json()['items']

    def get_vacancies(self, vacancy):
        self.params['text'] = vacancy
        data = self.get_response()
        self.vacancies.extend(data)

    @staticmethod
    def experience(vac):
        hh_experience = {"Нет опыта": "Без опыта",
                         "От 1 года до 3 лет": 'От 1 года',
                         "От 3 до 6 лет": 'От 3 лет',
                         "Более 6 лет": 'От 6 лет'
                         }
        return hh_experience[vac]

    def get_formatted_vacancies(self):
        """
        Получение некоторых полей вакансий
        """
        formatted_vacancies = []
        for vac in self.vacancies:
            formatted_vacancies.append({
                'name': vac['name'],
                'area': vac['area']['name'],
                'salary_from': vac['salary']['from'] if vac['salary'] else None,
                'salary_to': vac['salary']['to'] if vac['salary'] else None,
                'currency': vac['salary']['currency'].lower() if vac['salary'] else None,
                'experience': self.experience(vac['experience']['name']),
                'url': vac['alternate_url']
            })
        return formatted_vacancies


class SuperJobAPI(API):
    """
    Класс для работы с API superjob.ru
    """

    def __init__(self, period=7):
        self.header = {'X-Api-App-Id': os.getenv('SJ_API_KEY')}
        self.params = {
            'keyword': None,
            'period': period,
            'no_agreement': 1,
            'count': 100,
            'page': 0
        }
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.vacancies = []

    def get_response(self):
        response = requests.get(self.url, headers=self.header, params=self.params)
        if not response.ok:
            raise SJResponseError
        return response.json()['objects']

    def get_vacancies(self, vacancy):
        self.params['keyword'] = vacancy
        data = self.get_response()
        self.vacancies.extend(data)

    def get_formatted_vacancies(self):
        """
        Получение некоторых полей вакансий
        """
        formatted_vacancies = []
        for vac in self.vacancies:
            formatted_vacancies.append({
                'name': vac['profession'],
                'area': vac['town']['title'],
                'salary_from': vac['payment_from'] if vac['payment_from'] >= 0 else None,
                'salary_to': vac['payment_to'] if vac['payment_to'] > 0 else None,
                'currency': vac['currency'].lower(),
                'experience': vac['experience']['title'],
                'url': vac['link']
            })
        return formatted_vacancies
