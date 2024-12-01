import requests
import pytest

class TestUserAgent:

    expected_values = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mobile', 'No', 'Android'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1', 'Mobile', 'Chrome', 'iOS'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Googlebot', 'Unknown', 'Unknown'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0', 'Web', 'Chrome', 'No'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', 'Mobile', 'No', 'iPhone')
    ]

    @pytest.mark.parametrize("user_agent_value, platform_value, browser_value, device_value", expected_values)
    def test_check_user_agent(self, user_agent_value, platform_value, browser_value, device_value):
        payload = {'User-Agent': user_agent_value}
        response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=payload)

        assert response.json()["platform"] == platform_value, "Expected value of platform is not correct"
        assert response.json()["browser"] == browser_value, "Expected value of browser is not correct"
        assert response.json()["device"] == device_value, "Expected value of device is not correct"