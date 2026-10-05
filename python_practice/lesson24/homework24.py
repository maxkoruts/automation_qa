import logging
import os
import sys

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
USERNAME = "test_user"
PASSWORD = "test_pass"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_search.log")


# Логування: і в консоль, і у файл test_search.log

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("test_search")
    logger.setLevel(logging.INFO)

    # Щоб не дублювати обробники при повторному імпорті
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()


# Фікстура первинної аутентифікації (один раз на клас)

@pytest.fixture(scope="class")
def auth_headers():
    logger.info("=== Первинна аутентифікація: POST %s/auth ===", BASE_URL)
    try:
        response = requests.post(
            f"{BASE_URL}/auth", auth=(USERNAME, PASSWORD), timeout=10
        )
    except requests.exceptions.ConnectionError:
        logger.error("Сервер недоступний. Запустіть: python cars_app.py")
        pytest.fail("Сервер cars_app.py не запущено на 127.0.0.1:8080")

    logger.info("Статус аутентифікації: %s", response.status_code)
    assert response.status_code == 200, f"Не вдалося отримати токен: {response.text}"

    token = response.json()["access_token"]
    logger.info("Токен отримано (перші 15 символів): %s...", token[:15])
    return {"Authorization": f"Bearer {token}"}



# Тести

class TestCarsSearch:
    """
    Параметри: sort_by, limit, expected_count, order_key
    order_key - поле, за яким перевіряємо порядок (None - порядок не перевіряємо).
    """

    @pytest.mark.parametrize(
        "sort_by, limit, expected_count, order_key",
        [
            pytest.param("price", 5, 5, "price", id="price-limit5"),
            pytest.param("year", 3, 3, "year", id="year-limit3"),
            pytest.param("engine_volume", 10, 10, "engine_volume", id="engine-limit10"),
            pytest.param("brand", 7, 7, "brand", id="brand-limit7"),
            pytest.param(None, 4, 4, "brand", id="no-sort-limit4-default-brand"),
            pytest.param("price", None, 25, "price", id="price-no-limit"),
            pytest.param("color", 3, 3, None, id="unknown-field-limit3"),
        ],
    )
    def test_search_cars(
        self, auth_headers, sort_by, limit, expected_count, order_key
    ):
        params = {}
        if sort_by is not None:
            params["sort_by"] = sort_by
        if limit is not None:
            params["limit"] = limit

        logger.info("--- Запит GET /cars з параметрами: %s ---", params)
        response = requests.get(
            f"{BASE_URL}/cars", headers=auth_headers, params=params, timeout=10
        )
        logger.info("URL: %s", response.url)
        logger.info("Статус відповіді: %s", response.status_code)

        assert response.status_code == 200

        cars = response.json()
        logger.info("Отримано авто: %d -> %s", len(cars), [c["brand"] for c in cars])

        assert len(cars) == expected_count, (
            f"Очікували {expected_count} авто, отримали {len(cars)}"
        )

        if order_key:
            values = [car[order_key] for car in cars]
            logger.info("Значення поля '%s': %s", order_key, values)
            assert values == sorted(values), (
                f"Список не відсортовано за '{order_key}': {values}"
            )

        logger.info("Тест пройдено успішно")