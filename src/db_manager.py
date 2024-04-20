import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager:
    def __init__(self, dbname, user, password, host):
        """Инициализация класса"""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    @staticmethod
    def get_companies_and_vacancies_count(conn):
        """Статический метод для получения списка всех компаний и количество вакансий у каждой компании"""
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.title AS Наименование_компании, COUNT(vacancies.vacancies_id) "
                            "AS Количество_вакансий "
                            "FROM employers "
                            "INNER JOIN vacancies USING(employers_id) "
                            "GROUP BY employers.title "
                            "ORDER BY Количество_вакансий")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_all_vacancies(conn):
        """Статический метод для получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.title, vacancies.name, vacancies.salary_from, vacancies.salary_to, "
                            "vacancies.alternate_url FROM employers INNER JOIN vacancies USING(employers_id)")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_avg_salary(conn):
        """Статический метод для получения средней зарплаты по вакансиям"""
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from) AS AVG_salary_from, AVG(salary_to) AS AVG_salary_to "
                            "FROM vacancies")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_vacancies_with_higher_salary(conn):
        """Статический метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_vacancies_with_keyword(conn, word):
        """Статический метод для получения списка всех вакансий,
        в названии которых содержатся переданные в метод слова"""
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies WHERE name LIKE '%{word}%'")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def connect_db_request(self):
        """Метод подключение к базе данных для заполнения или получения информации"""
        conn = psycopg2.connect(host=self.host, database=self.dbname, user=self.user, password=self.password)
        return conn

    def connect_create_db(self):
        """Метод подключения к postgres, для создания БД"""
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password)
        return conn

    @staticmethod
    def create_bd(conn, name_db):
        """Статический метод для создания БД"""
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute(f"CREATE DATABASE {name_db}")
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def create_table_employers(conn):
        """Статический метод для создания таблицы работодатели"""
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"CREATE TABLE employers ("
                            f"employers_id serial NOT NULL,"
                            f"title varchar(50),"
                            f"city varchar(30),"
                            f"country varchar(20),"
                            f"description text,"
                            f"industries text,"
                            f"CONSTRAINT pk_employers PRIMARY KEY (employers_id))")
            print(f'Таблица employers успешно создана')

    @staticmethod
    def create_table_vacancies(conn):
        """Статический метод для создания таблицы вакансии"""
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"CREATE TABLE vacancies ("
                            f"vacancies_id serial NOT NULL,"
                            f"employers_id int NOT NULL,"
                            f"name varchar(100),"
                            f"city varchar(50),"
                            f"salary_from int,"
                            f"salary_to int,"
                            f"requirement text,"
                            f"description text,"
                            f"vacancy_type varchar(20),"
                            f"address varchar(150),"
                            f"schedule varchar(20),"
                            f"experience varchar(50),"
                            f"alternate_url varchar(100),"
                            f"CONSTRAINT pk_vacancies PRIMARY KEY (vacancies_id),"
                            f"CONSTRAINT fk_vacancies_employers FOREIGN KEY (employers_id) REFERENCES employers)")
            print(f'Таблица vacancies успешно создана')

    @staticmethod
    def insert_table(conn, data, name_table, params):
        """Статический метод для заполнения таблиц информацией"""
        with conn:
            with conn.cursor() as cur:
                for row in data:
                    cur.execute(f"INSERT INTO {name_table} VALUES ({params})", row)
        return print(f"Данные успешно добавлены в таблицу {name_table}")
