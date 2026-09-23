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


# Створюємо об'єкт класу "Студент"
student = Student("Максим", "Коруц", 20, 4.1)

# Виводимо початкову інформацію про студента
print("Інформація про студента:")
print(student)

# Змінюємо середній бал
student.change_average_grade(4.8)

# Виводимо оновлену інформацію
print("\nПісля зміни середнього балу:")
print(student)