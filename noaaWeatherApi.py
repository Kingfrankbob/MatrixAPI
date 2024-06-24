import requests

class NOAAWeather:
    def __init__(self, city = 'bartlesville'):
        self.city = city
        self.alertZone = None
        self.lat, self.lon = self.get_lat_and_long(city)
        self.forecast_url = self.get_forecast_url(self.lat, self.lon)

    
    def get_weather(self):
        if not self.forecast_url:
            return
        response = requests.get(self.forecast_url)
        data = response.json()
        periods = data['properties']['periods']
        for period in periods:
            if period['number'] == 1:
                temperature = period['temperature']
                windSpeed = period['windSpeed']
                windDirection = period['windDirection']
                shortForecast = period['shortForecast']
                relativeHumidity = period['relativeHumidity']['value']
                windSpeed_value = float(windSpeed.split()[0])

            weather_json = {
                'temperature': temperature,
                'windSpeed': windSpeed_value,
                'windDirection': windDirection,
                'windDegree': self.convert_wind_direction(windDirection),
                'shortForecast': shortForecast,
                'relativeHumidity': relativeHumidity,
                'perceivedTemperature': round(self.calculate_perceived_temperature(temperature, windSpeed_value, relativeHumidity), 1)  
                       
            }
            return weather_json
    
    def get_alerts(self):
        url = f'https://api.weather.gov/alerts/active/zone/{self.alertZone}'
        response = requests.get(url)
        data = response.json()
        if data['features']:
            alerts = data['features']
            for alert in alerts:
                alert_data = {
                    # 'headline': alert['properties']['headline'],
                    # 'description': alert['properties']['description'],
                    'severity': alert['properties']['severity'],
                    'event': alert['properties']['event'],
                    'effective': alert['properties']['effective'],
                    'expires': alert['properties']['expires']
                }
                return alert_data
        else:
            return None

    def convert_wind_direction(self, windDirection):
        #Convert wind directions from cardinal to degrees
        windDirections = {
            'N': 0,
            'NNE': 22.5,
            'NE': 45,
            'ENE': 67.5,
            'E': 90,
            'ESE': 112.5,
            'SE': 135,
            'SSE': 157.5,
            'S': 180,
            'SSW': 202.5,
            'SW': 225,
            'WSW': 247.5,
            'W': 270,
            'WNW': 292.5,
            'NW': 315,
            'NNW': 337.5
        }
        return windDirections.get(windDirection, None)

    def calculate_perceived_temperature(self, temperature, windSpeed, relativeHumidity):
        # Convert wind speed from mph to m/s
        windSpeed_m_s = windSpeed * 0.44704
        
        # Heat Index calculation (for high temperatures)
        if temperature >= 80 and relativeHumidity > 40:
            heatIndex = -42.379 + 2.04901523 * temperature + 10.14333127 * relativeHumidity \
                        - 0.22475541 * temperature * relativeHumidity - 6.83783e-3 * temperature**2 \
                        - 5.481717e-2 * relativeHumidity**2 + 1.22874e-3 * temperature**2 * relativeHumidity \
                        + 8.5282e-4 * temperature * relativeHumidity**2 - 1.99e-6 * temperature**2 * relativeHumidity**2
            return heatIndex
        
        # Wind Chill calculation (for low temperatures)
        elif temperature <= 50:
            windChill = 35.74 + 0.6215 * temperature - 35.75 * windSpeed_m_s**0.16 \
                        + 0.4275 * temperature * windSpeed_m_s**0.16
            return windChill
        
        # If neither condition is met, return the actual temperature
        return temperature
     
    def get_forecast_url(self, lat = 36.7421089, lon = -95.9528877):
        url = f'https://api.weather.gov/points/{lat},{lon}'
        response = requests.get(url)
        data = response.json()
        title = data.get('title', None)
        if title == 'Data Unavailable For Requested Point':
            print(f"Error: {title}")
            return
        else:
            self.alertZone = data['properties']['forecastZone'].split('/')[-1]
            return data['properties']['forecastHourly']
    

    def get_lat_and_long(self, city):
        url = f'https://nominatim.openstreetmap.org/search?q={city}&format=json'
        headers = {
            'User-Agent': 'MatrixWeather/1.0'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    print(f"Error: No data found for {city}")
                    return
                for location in data:
                    lat = location['lat']
                    lon = location['lon']
                    return lat, lon
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    NOAAWeather = NOAAWeather('Carbon')
    NOAAWeather.get_weather()
    NOAAWeather.get_alerts()