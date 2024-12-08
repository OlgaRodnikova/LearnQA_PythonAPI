import time
import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):
    def test_delete_user_with_id_2(self):
        login_data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }
        response_1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")

        response_2 = requests.delete(
            "https://playground.learnqa.ru/api/user/2",
            cookies = {"auth_sid": auth_sid},
            headers = {"x-csrf-token": token}
        )

        Assertions.assert_code_status(response_2, 400)
        Assertions.assert_json_value_by_name(
            response_2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Unexpected error"
        )

    def test_delete_user_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_1, 'id')

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response_2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_2, "auth_sid")
        token = self.get_header(response_2, "x-csrf-token")

        #DELETE
        response_3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_code_status(response_3, 200)

        #GET DATA
        response_4 = requests.get("https://playground.learnqa.ru/api/user/{user_id}")
        Assertions.assert_code_status(response_4, 404)

    def test_delete_user_by_another_user(self):
        register_data_1 = self.prepare_registration_data()
        response_1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_1)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, 'id')

        email_1 = register_data_1['email']
        password_1 = register_data_1['password']

        # REGISTER SECOND USER
        time.sleep(1)
        register_data_2 = self.prepare_registration_data()
        response_2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_2)

        Assertions.assert_code_status(response_2, 200)
        Assertions.assert_json_has_key(response_2, 'id')

        user_id_2 = self.get_json_value(response_2, 'id')

        # LOGIN AS FIRST USER
        login_data = {
            "email": email_1,
            "password": password_1
        }
        response_3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response_3, "auth_sid")
        token = self.get_header(response_3, "x-csrf-token")

        # DELETE SECOND USER
        response_4 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id_2}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_code_status(response_4, 400)
        Assertions.assert_json_value_by_name(
            response_4,
            "error",
            "This user can only delete their own account.",
            "Unexpected error"
        )
