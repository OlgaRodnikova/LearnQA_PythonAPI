from datetime import datetime
import pytest
import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserRegister(BaseCase):
    exclude_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def test_create_user_successfully(self):
        payload = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=payload)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        payload = self.prepare_registration_data(email = email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        payload = self.prepare_registration_data(email = email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('exclude_param', exclude_params)
    def test_create_user_without_one_param(self, exclude_param):
        data = self.prepare_registration_data()
        data.pop(exclude_param)
        payload = data

        response = requests.post("https://playground.learnqa.ru/api/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", f"Unexpected response content {response.content}"

    def test_create_user_with_too_short_username(self):
        username = 'a'
        payload = self.prepare_registration_data(username = username)
        response = requests.post("https://playground.learnqa.ru/api/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_too_long_username(self):
        username = 'test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name_test_long_name'
        payload = self.prepare_registration_data(username = username)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=payload)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", f"Unexpected response content {response.content}"
