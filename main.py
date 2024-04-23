from src.config import config
from src.head_hunter_api import HeadHunterAPI
from src.db_manager import DBManager as db
import src.utils as u

url = 'https://api.hh.ru/vacancies'
database_name = 'hh_ru'


def main():
    params = config()
    db.create_database(database_name, params)
    hh_api = HeadHunterAPI(url)
    vacancy = hh_api.get_employer_vacancies(113)
    data = u.filling_classes(vacancy)
    db.save_data_to_database(data, database_name, params)
    n = ''
    while n != 0:
        print('Меню программы:')
        exit_menu = int(input("1 - Вывод компании и количество их вакансий\n"
                              "2 - Вывод всех вакансий\n"
                              "3 - Вывод средней заработной платы\n"
                              "4 - Вывод вакансий с заработной платной выше средней\n"
                              "5 - Вывод вакансий по заданному слову в наименовании\n"
                              "0 - Выход\n"))

        if exit_menu == 1:
            db.get_companies_and_vacancies_count(database_name, params)
        elif exit_menu == 2:
            db.get_all_vacancies(database_name, params)
        elif exit_menu == 3:
            db.get_avg_salary(database_name, params)
        elif exit_menu == 4:
            db.get_vacancies_with_higher_salary(database_name, params)
        elif exit_menu == 5:
            word = input('Введите поисковое слово:\n').title()
            db.get_vacancies_with_keyword(database_name, params, word)
        else:
            n = 0
            print("Программа завершила работу!")

    # for item in data:
    #     for i in range(0, len(item.vacancies)):
    #         print(item.vacancies[i].vacancy_id)


if __name__ == '__main__':
    main()
