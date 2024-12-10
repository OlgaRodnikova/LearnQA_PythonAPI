import time
import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Редактирование пользователей по id")
class TestUserEdit(BaseCase):
    @allure.title("Редактирование пользователя: позитивный сценарий")
    @allure.description("Тест проверяет редактирование созданного пользователя")
    @allure.severity('blocker')
    def test_edit_just_create_user(self):
        with allure.step("Создание нового пользователя"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        with allure.step("Авторизация пользователя"):
            login_data = {
                "email": email,
                "password": password
            }
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Редактирование созданного пользователя"):
            new_name = 'Changed name'
            response3 = MyRequests.put(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response3, 200)

        with allure.step("Проверка результата редактирования: получение данных пользователя"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    @allure.title("Редактирование не авторизованного пользователя")
    @allure.description("Тест проверяет, что нельзя отредактировать данные не авторизованного пользователя")
    @allure.severity('blocker')
    def test_edit_user_not_auth(self):
        new_name = 'Changed name'
        response = MyRequests.put("/user/2", data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Auth token not supplied",
            "Unexpected error"
        )

    @allure.title("Редактирование УЗ другого пользователя")
    @allure.description("Тест проверяет, что нельзя отредактировать пользователя будучи авторизованным другим пользователем")
    @allure.severity('blocker')
    def test_edit_user_by_another_user(self):
        with allure.step("Создание пользователя 1"):
            register_data_1 = self.prepare_registration_data()
            response_1 = MyRequests.post("/user/", data=register_data_1)

            Assertions.assert_code_status(response_1, 200)
            Assertions.assert_json_has_key(response_1, 'id')

            email_1 = register_data_1['email']
            password_1 = register_data_1['password']

        with allure.step("Создание пользователя 2"):
            time.sleep(1)
            register_data_2 = self.prepare_registration_data()
            response_2 = MyRequests.post("/user/", data=register_data_2)

            Assertions.assert_code_status(response_2, 200)
            Assertions.assert_json_has_key(response_2, 'id')

            user_id_2 = self.get_json_value(response_2, 'id')

        with allure.step("Авторизация под УЗ пользователя 1"):
            login_data = {
                "email": email_1,
                "password": password_1
            }
            response_3 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response_3, "auth_sid")
            token = self.get_header(response_3, "x-csrf-token")

        with allure.step("Попытка отредактировать пользователя 2 под УЗ пользователя 1"):
            new_name = 'Changed name'
            response_4 = MyRequests.put(
                f"/user/{user_id_2}",
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

    @allure.title("Редактирование пользователя: некорректные входные данные")
    @allure.description(
        "Тест проверяет валидность входных данных при редактировании пользователя")
    @allure.severity('critical')
    def test_edit_auth_user_with_incorrect_data(self):
        with allure.step("Создание пользователя"):
            register_data = self.prepare_registration_data()
            response_1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response_1, 200)
            Assertions.assert_json_has_key(response_1, 'id')

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response_1, 'id')

        with allure.step("Авторизация пользователя"):
            login_data = {
                "email": email,
                "password": password
            }
            response_2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response_2, "auth_sid")
            token = self.get_header(response_2, "x-csrf-token")

        with allure.step("Проверка, что нельзя изменить email пользователя на некорректное значение (без @)"):
            new_email = 'vinkotovexample.com'
            response_3 = MyRequests.put(
                f"/user/{user_id}",
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

        with allure.step("Проверка, что нельзя изменить параметр 'firstName' на слишком короткое значение"):
            new_first_name = 'a'
            response_4 = MyRequests.put(
                f"/user/{user_id}",
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

