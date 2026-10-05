import os
import random

from sqlalchemy import Column, ForeignKey, Table, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


# =========================
# МОДЕЛІ
# =========================

class Base(DeclarativeBase):
    pass


enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("course_id", ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    courses: Mapped[list["Course"]] = relationship(
        secondary=enrollments,
        back_populates="students"
    )

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(255), default="")

    students: Mapped[list[Student]] = relationship(
        secondary=enrollments,
        back_populates="courses"
    )

    def __repr__(self):
        return f"{self.id}: {self.title}"


# =========================
# ПОЧАТКОВІ ДАНІ
# =========================

COURSES = [
    ("Python", "Основи програмування на Python"),
    ("Бази даних", "SQL, реляційні моделі, ORM"),
    ("Алгоритми", "Структури даних та алгоритми"),
    ("Веб-розробка", "HTML, CSS, JavaScript, REST"),
    ("Машинне навчання", "Вступ до ML"),
]

FIRST_NAMES = [
    "Олена", "Іван", "Марія", "Андрій", "Софія",
    "Дмитро", "Анна", "Максим", "Юлія", "Богдан",
    "Катерина", "Тарас", "Ірина", "Олег", "Наталія",
    "Василь", "Оксана", "Сергій", "Вікторія", "Роман"
]

LAST_NAMES = [
    "Коваленко", "Шевченко", "Бондаренко", "Ткаченко", "Мельник",
    "Кравченко", "Олійник", "Поліщук", "Савчук", "Лисенко",
    "Руденко", "Мороз", "Гончар", "Паламарчук", "Харченко",
    "Волошин", "Бойко", "Мазур", "Левченко", "Петренко"
]


def seed_database(session):
    courses = [Course(title=t, description=d) for t, d in COURSES]
    session.add_all(courses)

    for i in range(20):
        student = Student(
            first_name=FIRST_NAMES[i],
            last_name=LAST_NAMES[i],
            email=f"student{i + 1}@university.edu"
        )

        student.courses = random.sample(
            courses,
            random.randint(1, 3)
        )

        session.add(student)

    session.commit()


# =========================
# СТУДЕНТИ
# =========================

def add_student(session, first_name, last_name, email):
    student = Student(
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    session.add(student)
    session.commit()

    return student


def update_student(session, student_id, **fields):
    student = session.get(Student, student_id)

    if not student:
        raise ValueError("Студента не знайдено")

    for key, value in fields.items():
        setattr(student, key, value)

    session.commit()
    return student


def delete_student(session, student_id):
    student = session.get(Student, student_id)

    if not student:
        raise ValueError("Студента не знайдено")

    session.delete(student)
    session.commit()


# =========================
# КУРСИ
# =========================

def enroll_student(session, student_id, course_title):
    student = session.get(Student, student_id)

    course = session.scalar(
        select(Course).where(Course.title == course_title)
    )

    if not student:
        raise ValueError("Студента не знайдено")

    if not course:
        raise ValueError("Курс не знайдено")

    student.courses.append(course)
    session.commit()


def update_course(session, course_id, **fields):
    course = session.get(Course, course_id)

    if not course:
        raise ValueError("Курс не знайдено")

    for key, value in fields.items():
        setattr(course, key, value)

    session.commit()
    return course


# =========================
# ЗАПИТИ
# =========================

def get_students_by_course(session, course_title):
    return session.scalars(
        select(Student)
        .join(Student.courses)
        .where(Course.title == course_title)
        .order_by(Student.last_name)
    ).all()


def get_courses_by_student(session, student_id):
    return session.scalars(
        select(Course)
        .join(Course.students)
        .where(Student.id == student_id)
        .order_by(Course.title)
    ).all()


# =========================
# MAIN
# =========================

def main():
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://student_user:student_pass@localhost:5432/students_db"
    )

    engine = create_engine(database_url)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        # Початкові дані
        seed_database(session)

        print("Курсів:", session.query(Course).count())
        print("Студентів:", session.query(Student).count())

        # Додаємо студента
        student = add_student(
            session,
            "Петро",
            "Іваненко",
            "petro@university.edu"
        )

        enroll_student(session, student.id, "Python")
        enroll_student(session, student.id, "Бази даних")

        print("\nНовий студент:", student)
        print("Курси:", get_courses_by_student(session, student.id))

        # Студенти курсу
        print("\nСтуденти на Python:")

        for student in get_students_by_course(session, "Python"):
            print(student)

        # Оновлення
        update_student(
            session,
            student.id,
            last_name="Іваненко-Мельник"
        )

        update_course(
            session,
            1,
            description="Python: від основ до ООП"
        )

        print("\nПісля оновлення:")
        print(session.get(Student, student.id))

        # Видалення
        delete_student(session, student.id)

        print("\nСтудента видалено")


if __name__ == "__main__":
    main()