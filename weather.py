import requests


def fetch_weather(city):
    API_KEY = "b0b8e027b2b84b4ca64203801242112"
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=uk"
    response = requests.get(url).json()
    if "current" in response:
        return f"Температура: {response['current']['temp_c']}°C\n{response['current']['condition']['text']}"
    return "Не вдалося отримати дані про погоду."
