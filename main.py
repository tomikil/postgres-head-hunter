from src.head_hunter_api import HeadHunterAPI
from src.db_manager import DBManager
import src.utils as u
import json

url = 'https://api.hh.ru/vacancies'


def main():

    n = ''
    connect = DBManager('name_bd', 'user', 'password', 'host')
    while n != 0:

        conn = DBManager('NULL', 'NULL', 'NULL', 'NULL')
        print('Меню программы:')
        exit_menu = int(input("1 - Создание базы данных\n"
                              "2 - Подключиться к базе данных\n"
                              "3 - Создание таблиц в базе данных\n"
                              "4 - Заполнить таблицы данными\n"
                              "5 - Вывод компании и количество их вакансий\n"
                              "6 - Вывод всех вакансий\n"
                              "7 - Вывод средней заработной платы\n"
                              "8 - Вывод вакансий с заработной платной выше средней\n"
                              "9 - Вывод вакансий по заданному слову в наименовании\n"
                              "0 - Выход\n"))
        if exit_menu == 1:
            name_bd = input('Введите имя базы данных:\n')
            user = input("Введите имя пользователя Postgres:\n")
            password = input("Введите пароль Postgres:\n")
            host = input("Введите хост Postgres:\n")
            conn = DBManager('NULL', user, password, host)
            conn.create_bd(conn.connect_create_db(), name_bd)
            print(f'База данных {name_bd} создана')
        elif exit_menu == 2:
            name_bd = input('Введите имя базы данных:\n')
            user = input("Введите имя пользователя Postgres:\n")
            password = input("Введите пароль Postgres:\n")
            host = input("Введите хост Postgres:\n")
            connect = DBManager(name_bd, user, password, host)
        elif exit_menu == 3:
            connect.create_table_employers(connect.connect_db_request())
            connect.create_table_vacancies(connect.connect_db_request())
        elif exit_menu == 4:
            hh_api = HeadHunterAPI(url)
            vacancy = hh_api.get_employer_vacancies(113)
            params_employers = "%s, %s, %s, %s, %s, %s"
            params_vacancies = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
            connect.insert_table(connect.connect_db_request(), u.get_list_employers(u.filling_classes(vacancy)),
                                 'employers', params_employers)
            connect.insert_table(connect.connect_db_request(), u.get_list_vacancies(u.filling_classes(vacancy)),
                                 'vacancies', params_vacancies)
        elif exit_menu == 5:
            connect.get_companies_and_vacancies_count(connect.connect_db_request())
        elif exit_menu == 6:
            connect.get_all_vacancies(connect.connect_db_request())
        elif exit_menu == 7:
            connect.get_avg_salary(connect.connect_db_request())
        elif exit_menu == 8:
            connect.get_vacancies_with_higher_salary(connect.connect_db_request())
        elif exit_menu == 9:
            word = input('Введите поисковое слово:\n')
            connect.get_vacancies_with_keyword(connect.connect_db_request(), word)
        else:
            n = 0
            print("Программа завершила работу!")


if __name__ == '__main__':
    main()
