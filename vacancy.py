class Vacancy:
    """
    Класс для работы с вакансиями. В этом классе самостоятельно определить атрибуты,
    такие как название вакансии, ссылка на вакансию, зарплата, краткое описание или требования.
    Класс должен поддерживать методы сравнения вакансий между собой по зарплате и валидировать данные,
    которыми инициализируются его атрибуты.
    """
    def __init__(self, name, area, salary_from, salary_to, currency, experience, url):
        self.name = name
        self.area = area
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.experience = experience
        self.url = url

    @property
    def salary(self):
        if self.salary_to is None and self.salary_from is None:
            return 'Не указано'
        salary_from = self.salary_from if self.salary_from else None
        salary_to = self.salary_to if self.salary_to else None
        currency = self.currency if self.currency else None

        if salary_to is None:
            return f'От {salary_from} {currency}'
        elif salary_from is None:
            return f'До {salary_to} {currency}'
        return f'От {salary_from} до {salary_to} {currency}'

    def __str__(self):
        return f'Наименование вакансии: {self.name}\n' \
               f'Город: {self.area}\n' \
               f'Заработная плата: {self.salary}\n' \
               f'Требуемый опыт работы: {self.experience}\n' \
               f'Ссылка на вакансию: {self.url}\n\n'

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            if not self.salary_from:
                return True
            elif not other.salary_from:
                return False
            return self.salary_from < other.salary_from
