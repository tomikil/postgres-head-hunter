from abc import ABC, abstractmethod


class HeadHunterAPIAbstract(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass
