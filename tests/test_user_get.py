import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")
        Assertions.assert_json_has_not_key(response, "email")

    def test_get_user_details_auth_as_same_user(self):
        payload = {"email": "vinkotov@example.com", "password": "1234"}
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=payload)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_another_user(self):
        payload = {"email": "vinkotov@example.com", "password": "1234"}
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=payload)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        print(f"user_id = {user_id_from_auth_method}")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/1",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")
        Assertions.assert_json_has_not_key(response2, "email")


