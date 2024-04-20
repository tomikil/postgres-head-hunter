from src.employers import Employers
from src.vacancyes import Vacancies
import re


def filling_classes(employers):
    """Заполнения класса работодателей и класс вакансии"""
    list_employers = []

    for employee in employers:
        list_vacancies = []
        for number in range(0, len(employee['vacancies'])):
            for item in range(0, len(employee['vacancies'][number])):
                salary_from = 0
                salary_to = 0
                if employee['vacancies'][number][item]['salary'] is None:
                    salary_from = 0
                    salary_to = 0
                elif employee['vacancies'][number][item]['salary']['from'] is None:
                    salary_from = 0
                    salary_to = employee['vacancies'][number][item]['salary']['to']
                elif employee['vacancies'][number][item]['salary']['to'] is None:
                    salary_from = employee['vacancies'][number][item]['salary']['from']
                    salary_to = 0
                else:
                    salary_from = employee['vacancies'][number][item]['salary']['from']
                    salary_to = employee['vacancies'][number][item]['salary']['to']
                address = ''
                if employee['vacancies'][number][item]['address'] is None:
                    address = 'NULL'
                else:
                    address = employee['vacancies'][number][item]['address']['raw']
                list_vacancies.append(
                    Vacancies(employee['vacancies'][number][item]['id'], employee['vacancies'][number][item]['name'],
                              employee['vacancies'][number][item]['area']['name'], salary_from, salary_to,
                              employee['vacancies'][number][item]['snippet']['requirement'],
                              employee['vacancies'][number][item]['snippet']['responsibility'],
                              employee['vacancies'][number][item]['type']['name'],
                              address, employee['vacancies'][number][item]['schedule']['name'],
                              employee['vacancies'][number][item]['experience']['name'],
                              employee['vacancies'][number][item]['alternate_url']))
        list_employers.append(Employers(employee['employers']['id'], employee['employers']['name'],
                                        employee['employers']['area']['name'], 'Россия',
                                        re.sub(r'<.*?>', '', str(employee['employers']['description'])),
                                        employee['employers']['industries'][0]['name'],
                                        list_vacancies))
    return list_employers


def get_list_employers(employers):
    """Получение списка работодателей с информацией из класса для заполнения БД"""
    rows = []
    for item in employers:
        rows.append([item.employers_id, item.title, item.city, item.country, item.description, item.industries])
    return rows


def get_list_vacancies(employers):
    """Получение списка вакансий с информацией из класса для заполнения БД"""
    rows = []
    for item in employers:
        for i in range(0, len(item.vacancies)):
            rows.append(
                [item.vacancies[i].vacancy_id, item.employers_id, item.vacancies[i].name, item.vacancies[i].city,
                 item.vacancies[i].salary_from, item.vacancies[i].salary_to, item.vacancies[i].requirement,
                 item.vacancies[i].description, item.vacancies[i].vacancy_type, item.vacancies[i].address,
                 item.vacancies[i].schedule, item.vacancies[i].experience, item.vacancies[i].alternate_url])
    return rows
