import requests
import time

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserEdit(BaseCase):
    def test_edit_just_create_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        #LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = 'Changed name'
        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_not_auth(self):
        new_name = 'Changed name'
        response = requests.put("https://playground.learnqa.ru/api/user/2", data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Auth token not supplied",
            "Unexpected error"
        )

    def test_edit_user_by_another_user(self):
        #REGISTER FIRST USER
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

        # EDIT SECOND USER
        new_name = 'Changed name'
        response_4 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id_2}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_4, 400)
        Assertions.assert_json_value_by_name(
            response_4,
            "error",
            "This user can only edit their own data.",
            "Unexpected error"
        )

    def test_edit_auth_user_with_incorrect_data(self):
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

        # EDIT EMAIL
        new_email = 'vinkotovexample.com'
        response_3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response_3, 400)
        Assertions.assert_json_value_by_name(
            response_3,
            "error",
            "Invalid email format",
            "Unexpected error"
        )

        # EDIT FirstName
        new_first_name = 'a'
        response_4 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(response_3, 400)
        Assertions.assert_json_value_by_name(
            response_4,
            "error",
            "The value for field `firstName` is too short",
            "Unexpected error"
        )

