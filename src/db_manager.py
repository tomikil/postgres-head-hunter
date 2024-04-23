import psycopg2


class DBManager:
    @staticmethod
    def create_database(database_name: str, params: dict) -> None:
        """Метод создание БД и таблиц"""
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute(f"CREATE TABLE employers ("
                        f"employers_id serial NOT NULL,"
                        f"title varchar(50),"
                        f"city varchar(30),"
                        f"country varchar(20),"
                        f"description text,"
                        f"industries text,"
                        f"CONSTRAINT pk_employers PRIMARY KEY (employers_id)"
                        f")"
                        )

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
                        f"experience varchar(150),"
                        f"alternate_url varchar(100),"
                        f"CONSTRAINT pk_vacancies PRIMARY KEY (vacancies_id),"
                        f"CONSTRAINT fk_vacancies_employers FOREIGN KEY (employers_id) REFERENCES employers)")
        conn.commit()
        conn.close()

    @staticmethod
    def save_data_to_database(data, database_name: str, params: dict) -> None:
        """Метод для заполнения таблиц данными"""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            for employers in data:
                cur.execute(f"INSERT INTO employers VALUES (%s, %s, %s, %s, %s, %s) "
                            f"RETURNING employers_id", (employers.employers_id, employers.title, employers.city,
                                                        employers.country, employers.description, employers.industries))

                employers_id = cur.fetchone()[0]
                vacancies = employers.vacancies
                for i in range(0, len(employers.vacancies)):
                    cur.execute(f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (vacancies[i].vacancy_id, employers_id,
                                 vacancies[i].name, vacancies[i].city,
                                 vacancies[i].salary_from, vacancies[i].salary_to,
                                 vacancies[i].requirement, vacancies[i].description,
                                 vacancies[i].vacancy_type, vacancies[i].address,
                                 vacancies[i].schedule, vacancies[i].experience,
                                 vacancies[i].alternate_url))
        conn.commit()
        conn.close()

    @staticmethod
    def get_companies_and_vacancies_count(database_name: str, params: dict) -> None:
        """Статический метод для получения списка всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(dbname=database_name, **params) as conn:
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
    def get_all_vacancies(database_name: str, params: dict) -> None:
        """Статический метод для получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT employers.title, vacancies.name, vacancies.salary_from, vacancies.salary_to, "
                            "vacancies.alternate_url FROM employers INNER JOIN vacancies USING(employers_id)")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_avg_salary(database_name: str, params: dict) -> None:
        """Статический метод для получения средней зарплаты по вакансиям"""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from) AS AVG_salary_from, AVG(salary_to) AS AVG_salary_to "
                            "FROM vacancies")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_vacancies_with_higher_salary(database_name: str, params: dict) -> None:
        """Статический метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    @staticmethod
    def get_vacancies_with_keyword(database_name: str, params: dict, word: str) -> None:
        """Статический метод для получения списка всех вакансий,
        в названии которых содержатся переданные в метод слова"""
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies WHERE name LIKE '%{word}%'")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
