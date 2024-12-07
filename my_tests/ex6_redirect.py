import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

number_of_redirects = len(response.history)
print(f"Количество редиректов в запросе равно {number_of_redirects}")

url_final = response.url
print(f"Итоговый URL {url_final}")