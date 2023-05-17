class HHResponseError(Exception):
    """
    Класс ошибки при некорректном ответе hh.ru
    """
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Ошибка ответа HeadHunter.'


class SJResponseError(Exception):
    """
    Класс ошибки при некорректном ответе superjob.ru
    """
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Ошибка ответа SuperJob.'
