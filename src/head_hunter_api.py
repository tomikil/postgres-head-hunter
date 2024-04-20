import requests
import time


class HeadHunterAPI:
    def __init__(self, url):
        """Инициализация класса"""
        self.url = url

    def connect(self):
        """Проверка на доступность сайта"""
        response = requests.get(self.url)
        return response.status_code

    def get_employer_vacancies(self, areas):
        """Получение списка работодателей со списком их вакансий """
        try:
            if self.connect() != 200:
                raise NameError(f"Ошибка подключения, статус ошибки: {self.connect()}")
            else:
                list_employers_id = [3529, 1740, 64174, 15478, 4181, 2180, 78638, 1429999, 1122462, 41862]

                list_employers = []
                for employer in list_employers_id:
                    list_vacancies = []
                    employers = requests.get(f"https://api.hh.ru/employers/{employer}")
                    employers_json = employers.json()
                    for page in range(0, 20):
                        vacancy = requests.get(f"https://api.hh.ru/vacancies?employer_id={employer}",
                                               params={'areas': areas, 'page': page, 'per_page': 100})
                        vacancy_json = vacancy.json()['items']
                        # for item in range(0, len(vacancy_json)):
                        list_vacancies.append(vacancy_json)
                        if (vacancy.json()['pages'] - page) <= 1:
                            break
                        time.sleep(0.25)
                    list_employers.append({'employers': employers_json, 'vacancies': list_vacancies})
                return list_employers
        except NameError:
            print(NameError)
