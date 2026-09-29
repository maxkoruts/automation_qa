import pytest


class Student:
    def __init__(self, first_name: str, last_name: str, age: int, average_grade: float):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.average_grade = average_grade

    def change_average_grade(self, new_grade: float):
        """
        Змінює середній бал студента на нове значення.
        """
        self.average_grade = new_grade

    def __str__(self):
        return (f"Ім'я: {self.first_name}\n"
                f"Прізвище: {self.last_name}\n"
                f"Вік: {self.age}\n"
                f"Середній бал: {self.average_grade}")


@pytest.fixture
def student():
    return Student("Максим", "Коруц", 20, 4.1)


def test_створення_студента_зберігає_атрибути(student):
    """Усі значення з конструктора коректно зберігаються в атрибутах."""
    assert student.first_name == "Максим"
    assert student.last_name == "Коруц"
    assert student.age == 20
    assert student.average_grade == 4.1


def test_зміна_середнього_балу(student):
    """Метод change_average_grade замінює середній бал на нове значення."""
    student.change_average_grade(4.8)

    assert student.average_grade == 4.8


def test_зміна_балу_не_впливає_на_інші_поля(student):
    """Після зміни балу ім'я, прізвище та вік залишаються без змін."""
    student.change_average_grade(4.8)

    assert student.first_name == "Максим"
    assert student.last_name == "Коруц"
    assert student.age == 20


@pytest.mark.parametrize("new_grade", [0, 2.5, 5, 12.0])
def test_зміна_балу_для_різних_значень(student, new_grade):
    """Метод приймає різні значення балу й зберігає їх."""
    student.change_average_grade(new_grade)

    assert student.average_grade == new_grade


def test_str_повертає_очікуваний_текст(student):
    """Рядкове представлення містить усі дані студента, а після зміни балу оновлюється."""
    expected = (
        "Ім'я: Максим\n"
        "Прізвище: Коруц\n"
        "Вік: 20\n"
        "Середній бал: 4.1"
    )
    assert str(student) == expected

    student.change_average_grade(4.8)

    assert str(student).endswith("Середній бал: 4.8")