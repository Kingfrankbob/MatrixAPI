import requests
import json

class weather:
    # url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'
    def __init__(self):
         with open('config.json') as config:
            config = json.load(config)
            self.city = config['city']
            self.country = config['country']
            self.api_key = config['api_key']
            self.url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&appid={self.api_key}&units=metric'

    def get_weather_json(self):
        response = requests.get(self.url)
        data = response.json()

        if data['cod'] == 200:
            return {"data": data}
        else:
            return {"error": data}
    
if __name__ == '__main__':
    weather_class = weather()
    test = weather_class.get_weather_json()
    print(test)
