import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

@allure.epic("Создание пользователя")
class TestUserRegister(BaseCase):
    exclude_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.title("Создание пользователя: Позитивный сценарий")
    @allure.description("Тест проверяет успешное создание пользователя")
    @allure.severity('blocker')
    def test_create_user_successfully(self):
        payload = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=payload)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.title("Создание пользователя с уже существующим 'email'")
    @allure.description("Тест проверяет, что нельзя создать нового пользователя с уже существующим 'email'")
    @allure.severity('blocker')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        payload = self.prepare_registration_data(email = email)

        response = MyRequests.post("/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.title("Создание пользователя с некорректным 'email'")
    @allure.description("Тест проверяет, что нельзя создать нового пользователя с некорректным 'email' (без @)")
    @allure.severity('critical')
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        payload = self.prepare_registration_data(email = email)

        response = MyRequests.post("/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    @allure.title("Создание пользователя без указания 1 параметра")
    @allure.description("Тест проверяет, что нельзя создать нового пользователя без указания хотя бы одного обязательного параметра")
    @allure.severity('critical')
    @pytest.mark.parametrize('exclude_param', exclude_params)
    def test_create_user_without_one_param(self, exclude_param):
        data = self.prepare_registration_data()
        data.pop(exclude_param)
        payload = data

        response = MyRequests.post("/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", f"Unexpected response content {response.content}"

    @allure.title("Создание пользователя с коротким значением параметра 'username'")
    @allure.description("Тест проверяет, что нельзя создать нового пользователя с слишком коротким значением параметра 'username' (1 символ)")
    @allure.severity('major')
    def test_create_user_with_too_short_username(self):
        username = 'a'
        payload = self.prepare_registration_data(username = username)
        response = MyRequests.post("/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"

    @allure.title("Создание пользователя с длинным значением параметра 'username'")
    @allure.description(
        "Тест проверяет, что нельзя создать нового пользователя с слишком длинным значением параметра 'username' (>250 символов)")
    @allure.severity('major')
    def test_create_user_with_too_long_username(self):
        username = 'test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name'
        payload = self.prepare_registration_data(username = username)

        response = MyRequests.post("/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", f"Unexpected response content {response.content}"
