import requests

class TestHeaders:
    def test_get_headers(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)

        assert 'x-secret-homework-header' in response.headers, "There is no 'x-secret-homework-header' header in the response"

        expected_header_value = "Some secret value"
        actual_header_value = response.headers['x-secret-homework-header']

        assert actual_header_value == expected_header_value, "Actual value of 'x-secret-homework-header' header is not correct"