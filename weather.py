import requests

api_key = 'ba3129d08bdc643c2aba377243ae3fc1'
city = 'Bartlesville'
country = 'US'
url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'

def get_weather_json():
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        return {"data": data}
    else:
        return {"error": data}
    
if __name__ == '__main__':
    test = get_weather_json()
    print(test)
