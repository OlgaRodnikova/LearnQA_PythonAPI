import requests

response_1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ без параметра method: {response_1.text}\n")

response_2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ для неподдерживаемого метода head: {response_2.text}\n")

payload_3 = {"method": "GET"}
response_3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload_3)
print(f"Ответ при совпадении метода со значением параметра method {response_3.text}\n")

list_of_methods = ['GET', 'POST', 'PUT', 'DELETE']
for method_value in list_of_methods:
    payload = {"method": method_value}
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
    print(f"Ответ на запрос GET с параметром method {method_value}: {response_get.text}")
print("\n")

for method_value in list_of_methods:
    payload = {"method": method_value}
    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f"Ответ на запрос POST с параметром method {method_value}: {response_post.text}")
print("\n")

for method_value in list_of_methods:
    payload = {"method": method_value}
    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f"Ответ на запрос PUT с параметром method {method_value}: {response_put.text}")
print("\n")

for method_value in list_of_methods:
    payload = {"method": method_value}
    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f"Ответ на запрос DELETE с параметром method {method_value}: {response_delete.text}")