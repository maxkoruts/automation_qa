import logging

import pytest

from homework13 import log_event

LOGGER_NAME = "log_event"


#Фікстури

@pytest.fixture(autouse=True)
def clean_root_logger():
    """Ізолює тести: скидає хендлери root-логера до і після кожного тесту,
    щоб basicConfig міг спрацювати повторно."""
    root = logging.getLogger()
    saved_handlers = root.handlers[:]
    saved_level = root.level
    yield
    for h in root.handlers[:]:
        if h not in saved_handlers:
            h.close()
    root.handlers = saved_handlers
    root.setLevel(saved_level)


#Рівні логування

def test_success_logged_as_info(caplog):
    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        log_event("alice", "success")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.INFO


def test_expired_logged_as_warning(caplog):
    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        log_event("bob", "expired")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.WARNING


def test_failed_logged_as_error(caplog):
    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        log_event("carol", "failed")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.ERROR


@pytest.mark.parametrize(
    "status, expected_level",
    [
        ("success", logging.INFO),
        ("expired", logging.WARNING),
        ("failed", logging.ERROR),
    ],
)
def test_status_to_level_mapping(caplog, status, expected_level):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("user", status)

    assert [r.levelno for r in caplog.records] == [expected_level]


#Формат повідомлення

@pytest.mark.parametrize("status", ["success", "expired", "failed"])
def test_message_format(caplog, status):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("alice", status)

    assert caplog.records[0].getMessage() == (
        f"Login event - Username: alice, Status: {status}"
    )


def test_message_contains_username_and_status(caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("dave", "expired")

    message = caplog.records[0].getMessage()
    assert "dave" in message
    assert "expired" in message


def test_logger_name(caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("alice", "success")

    assert caplog.records[0].name == LOGGER_NAME


#Невідомі/некоректні статуси

@pytest.mark.parametrize(
    "status",
    ["unknown", "", "SUCCESS", "Failed", " success", "locked", "None"],
)
def test_unknown_status_falls_back_to_error(caplog, status):
    """Будь-який статус, окрім точних 'success' та 'expired', логується як error."""
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("alice", status)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.ERROR
    assert f"Status: {status}" in caplog.records[0].getMessage()


def test_none_status_falls_back_to_error(caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("alice", None)

    assert caplog.records[0].levelno == logging.ERROR
    assert "Status: None" in caplog.records[0].getMessage()


#Особливі імена користувачів

@pytest.mark.parametrize(
    "username",
    [
        "",
        "user with spaces",
        "користувач_укр",
        "user@example.com",
        "o'brien",
        "a" * 1000,
        "line1\nline2",
    ],
)
def test_various_usernames_are_logged(caplog, username):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event(username, "success")

    assert len(caplog.records) == 1
    assert f"Username: {username}," in caplog.records[0].getMessage()


def test_username_with_percent_signs_is_not_interpreted(caplog):
    """Повідомлення передається як готовий рядок, тому '%' не повинні ламати логування."""
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("100%s%d", "success")

    assert "Username: 100%s%d," in caplog.records[0].getMessage()


#Кількість записів

def test_each_call_produces_exactly_one_record(caplog):
    with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        log_event("a", "success")
        log_event("b", "expired")
        log_event("c", "failed")

    assert len(caplog.records) == 3
    assert [r.levelno for r in caplog.records] == [
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
    ]


#Конфігурація логера

def test_basic_config_called_with_expected_arguments(monkeypatch):
    calls = []
    monkeypatch.setattr(
        logging, "basicConfig", lambda **kwargs: calls.append(kwargs)
    )

    log_event("alice", "success")

    assert len(calls) == 1
    assert calls[0]["filename"] == "login_system.log"
    assert calls[0]["level"] == logging.INFO
    assert calls[0]["format"] == "%(asctime)s - %(message)s"


#Інтеграційний тест: запис у файл

def test_events_written_to_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Прибираємо хендлери (зокрема caplog/pytest), щоб basicConfig спрацював
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)

    log_event("alice", "success")
    log_event("bob", "expired")
    log_event("carol", "failed")

    for h in root.handlers:
        h.flush()

    log_file = tmp_path / "login_system.log"
    assert log_file.exists()

    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    assert lines[0].endswith("Login event - Username: alice, Status: success")
    assert lines[1].endswith("Login event - Username: bob, Status: expired")
    assert lines[2].endswith("Login event - Username: carol, Status: failed")
    # Формат: '<asctime> - <message>'
    assert all(" - Login event - " in line for line in lines)