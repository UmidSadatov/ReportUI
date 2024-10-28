import requests

# Заголовки для запроса
API_KEY = "82a5cbdb04e94d51baa100244242510"
CITY = "Tashkent"

# Параметры запроса
url = "http://api.weatherapi.com/v1"


def get_current():
    params = {
        "key": API_KEY,
        "q": CITY,
        "aqi": "yes"
    }

    response = requests.get(url, params=params)

    

# Выполняем запрос


# Проверка на успешность запроса
if response.status_code == 200:
    print(response.text)  # Выводим результат запроса
else:
    print(f"Ошибка: {response.status_code}")