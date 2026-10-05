import os
import time

import psycopg2

time.sleep(30)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)
print("Connected to the database!")

try:
    with conn:
        with conn.cursor() as cur:
            # 0. Створюємо таблицю (база порожня)
            cur.execute("DROP TABLE IF EXISTS test_items")
            cur.execute("""
                CREATE TABLE test_items (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    value INTEGER NOT NULL
                )
            """)
            print("Table created.")

            # 1. Додаємо 3 нових рядки
            cur.executemany(
                "INSERT INTO test_items (name, value) VALUES (%s, %s)",
                [("first", 1), ("second", 2), ("third", 3)],
            )
            print("Inserted 3 rows.")

            # 2. Оновлюємо один рядок
            cur.execute(
                "UPDATE test_items SET value = %s WHERE name = %s",
                (100, "first"),
            )
            print(f"Updated rows: {cur.rowcount}")

            # 3. Видаляємо інший рядок
            cur.execute("DELETE FROM test_items WHERE name = %s", ("second",))
            print(f"Deleted rows: {cur.rowcount}")

            # 4. Виводимо два рядки, що залишились
            cur.execute("SELECT id, name, value FROM test_items ORDER BY id")
            rows = cur.fetchall()
            print("Remaining rows:")
            for row in rows:
                print(row)

            assert len(rows) == 2, f"Expected 2 rows, got {len(rows)}"
            assert rows[0][1:] == ("first", 100)
            assert rows[1][1:] == ("third", 3)
            print("All checks passed!")
finally:
    conn.close()