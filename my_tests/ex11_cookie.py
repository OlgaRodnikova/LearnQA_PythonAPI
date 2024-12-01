import requests

class TestCookie:
    def test_get_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies)

        assert 'HomeWork' in response.cookies, "There is no 'HomeWork' cookie in the response"

        expected_cookie_value = "hw_value"
        actual_cookie_value = response.cookies.get('HomeWork')

        assert actual_cookie_value == expected_cookie_value, "Actual value of 'HomeWork' cookie is not correct"
