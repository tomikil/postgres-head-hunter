class Vacancies:
    def __init__(self, vacancy_id, name, city, salary_from, salaru_to, requirement, description, vacancy_type, address,
                 schedule, experience, alternate_url):
        """Инициализация класса"""
        self.vacancy_id = vacancy_id
        self.name = name
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salaru_to
        self.requirement = requirement
        self.description = description
        self.vacancy_type = vacancy_type
        self.address = address
        self.schedule = schedule
        self.experience = experience
        self.alternate_url = alternate_url
