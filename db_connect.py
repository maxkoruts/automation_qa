import os
import time

import allure
import psycopg2
import pytest

FEATURE = "Робота з PostgreSQL"


@pytest.fixture(scope="module")
def conn():
    """Підключення до БД з очікуванням її готовності (замість time.sleep(30))."""
    connection = None
    last_error = None
    with allure.step("Підключитися до бази даних"):
        for _ in range(30):
            try:
                connection = psycopg2.connect(
                    host=os.getenv("DB_HOST"),
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    port=os.getenv("DB_PORT"),
                )
                break
            except psycopg2.OperationalError as e:
                last_error = e
                time.sleep(1)
        if connection is None:
            pytest.fail(f"Не вдалося підключитися до БД: {last_error}")
        connection.autocommit = True
    yield connection
    connection.close()


@pytest.fixture
def cur(conn):
    """Курсор з чистою таблицею test_items для кожного тесту."""
    with conn.cursor() as cursor:
        with allure.step("Створити таблицю test_items"):
            cursor.execute("DROP TABLE IF EXISTS test_items")
            cursor.execute("""
                CREATE TABLE test_items (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    value INTEGER NOT NULL
                )
            """)
        yield cursor


def insert_rows(cur):
    with allure.step("Додати 3 нових рядки"):
        cur.executemany(
            "INSERT INTO test_items (name, value) VALUES (%s, %s)",
            [("first", 1), ("second", 2), ("third", 3)],
        )


def update_row(cur):
    with allure.step("Оновити рядок 'first' (value = 100)"):
        cur.execute(
            "UPDATE test_items SET value = %s WHERE name = %s",
            (100, "first"),
        )
        return cur.rowcount


def delete_row(cur):
    with allure.step("Видалити рядок 'second'"):
        cur.execute("DELETE FROM test_items WHERE name = %s", ("second",))
        return cur.rowcount


def select_all(cur):
    with allure.step("Отримати всі рядки"):
        cur.execute("SELECT id, name, value FROM test_items ORDER BY id")
        rows = cur.fetchall()
        allure.attach(
            "\n".join(str(r) for r in rows),
            name="Рядки в таблиці",
            attachment_type=allure.attachment_type.TEXT,
        )
        return rows


@allure.feature(FEATURE)
@allure.story("Створення таблиці")
def test_create_table(cur):
    rows = select_all(cur)
    with allure.step("Перевірити, що таблиця порожня"):
        assert rows == []


@allure.feature(FEATURE)
@allure.story("Вставка даних")
def test_insert_rows(cur):
    insert_rows(cur)
    rows = select_all(cur)
    with allure.step("Перевірити, що додано 3 рядки"):
        assert len(rows) == 3
        assert [r[1:] for r in rows] == [("first", 1), ("second", 2), ("third", 3)]


@allure.feature(FEATURE)
@allure.story("Оновлення даних")
def test_update_row(cur):
    insert_rows(cur)
    updated = update_row(cur)
    with allure.step("Перевірити, що оновлено рівно 1 рядок"):
        assert updated == 1
    rows = select_all(cur)
    with allure.step("Перевірити нове значення"):
        assert rows[0][1:] == ("first", 100)


@allure.feature(FEATURE)
@allure.story("Видалення даних")
def test_delete_row(cur):
    insert_rows(cur)
    deleted = delete_row(cur)
    with allure.step("Перевірити, що видалено рівно 1 рядок"):
        assert deleted == 1
    rows = select_all(cur)
    with allure.step("Перевірити, що рядка 'second' більше немає"):
        assert "second" not in [r[1] for r in rows]


@allure.feature(FEATURE)
@allure.story("Повний сценарій")
def test_full_scenario(cur):
    insert_rows(cur)
    update_row(cur)
    delete_row(cur)
    rows = select_all(cur)
    with allure.step("Перевірити, що залишилось 2 рядки з очікуваними даними"):
        assert len(rows) == 2, f"Expected 2 rows, got {len(rows)}"
        assert rows[0][1:] == ("first", 100)
        assert rows[1][1:] == ("third", 3)