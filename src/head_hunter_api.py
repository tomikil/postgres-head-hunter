from src.abstract_head_hunter_api import HeadHunterAPIAbstract
import requests
import time


class HeadHunterAPI(HeadHunterAPIAbstract):
    def __init__(self, url):
        self.url = url

    def connect(self):
        response = requests.get(self.url)
        return response.status_code

    def get_vacancies(self):
        try:
            if self.connect() != 200:
                raise NameError(f"Ошибка подключения, статус ошибки: {self.connect()}")
            else:
                list_employers_id = [3529, 1740, 64174, 15478, 4181, 2180, 78638, 1429999, 1122462, 41862]
                list_vacancies_employer = []
                for employer in list_employers_id:
                    for page in range(0, 20):
                        response = requests.get('https://api.hh.ru/vacancies',
                                                params={'employer_id': employer, 'area': 4,
                                                        'page': page, 'per_page': 100})
                        vacancy = response.json()['items']
                        list_vacancies_employer.append(vacancy)
                        if (response.json()['pages'] - page) <= 1:
                            break
                        time.sleep(0.25)
                return list_vacancies_employer
        except NameError:
            print(NameError)
