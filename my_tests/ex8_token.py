import requests
import time

response_1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
parsed_response_1 = response_1.json()
job_token = parsed_response_1['token']
seconds = parsed_response_1['seconds']

payload = {"token": job_token}
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)
print(response_2.text)

time.sleep(seconds)
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)
print(response_2.text)