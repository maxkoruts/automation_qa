import allure
import pytest


@allure.epic("API")
@allure.feature("QAAUTO feature")
@allure.story("Get user - negative")
@pytest.mark.qaauto_api
def test_get_current_negative(qa_auto_controller):
    response_current = qa_auto_controller.get_current(use_cookies=False, check_schema=False)
    print(response_current.json())
    assert response_current.status_code == 401
    assert response_current.json()["status"] == "error"