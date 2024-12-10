import time
import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

@allure.epic("Удаление пользователей по id")
class TestUserDelete(BaseCase):
    @allure.title("Удаление пользователя с id=2")
    @allure.description("Тест проверяет, что нельзя удалить пользователя с id=2")
    @allure.severity('critical')
    def test_delete_user_with_id_2(self):
        with allure.step("Авторизация пользователя с id=2"):
            login_data = {
                "email": 'vinkotov@example.com',
                "password": '1234'
            }
            response_1 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response_1, "auth_sid")
            token = self.get_header(response_1, "x-csrf-token")

        with allure.step("Попытка удалить пользователя с id=2"):
            response_2 = MyRequests.delete(
                "/user/2",
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

    @allure.title("Удаление пользователя: позитивный сценарий")
    @allure.severity('blocker')
    def test_delete_user_successfully(self):
        with allure.step("Создание нового пользователя"):
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

        with allure.step("Удаление созданного пользователя"):
            response_3 = MyRequests.delete(
                f"/user/{user_id}",
                cookies={"auth_sid": auth_sid},
                headers={"x-csrf-token": token}
            )

            Assertions.assert_code_status(response_3, 200)

        with allure.step("Проверка, что удаленный пользователь не существует"):
            response_4 = MyRequests.get("/user/{user_id}")
            Assertions.assert_code_status(response_4, 404)

    @allure.title("Удаление пользователя: негативный сценарий")
    @allure.description("Тест проверяет, что нельзя удалить пользователя будучи авторизованным другим пользователем")
    @allure.severity('blocker')
    def test_delete_user_by_another_user(self):
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

        with allure.step("Попытка удалить пользователя 2 под УЗ пользователя 1"):
            response_4 = MyRequests.delete(
                f"/user/{user_id_2}",
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
