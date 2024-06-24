from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from matrix import LEDMatrix
from weather import weather
from noaaWeatherApi import NOAAWeather
from pool import POOL_ART, pool_data

class MatrixAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        
        self.width = 64
        self.height = 64
        self.color_array = LEDMatrix(self.width, self.height)
        self.current_screen = "time"
        self.weather_request = NOAAWeather()
        self.pool_request = pool_data()
        self.index = 0

        self.update_screen()
        
        self.app.add_url_rule('/', 'hello_world', self.hello_world)
        self.app.add_url_rule('/api/frame', 'get_anim_frame', self.get_anim_frame, methods=['GET'])
        self.app.add_url_rule('/api/frame', 'set_anim_frame', self.set_anim_frame, methods=['POST'])

    def hello_world(self):
        return jsonify({'test': "This is Michael's API, feel free to ask for help on the \nHowever im more curious why your even here"}), 200
        
    def get_anim_frame(self):
        index = request.args.get('index', type=int)
        current_frame = self.color_array.matrix[index]
        return {'frame': current_frame}, 200

    def set_anim_frame(self):
        data = request.get_json()
        self.current_screen = data.get('type')
        self.update_screen()
        return jsonify({'message': f'Animation frame for {data.get("type")} set successfully'}), 200 

    def update_screen(self):
        if self.current_screen == "weather":
            self.weather()
        elif self.current_screen == "time":
            self.time()
        elif self.current_screen == "pool":
            self.pool()

    def weather(self):
        weather_data = self.weather_request.get_weather()
        if 'error' in weather_data:
            return
        
        # print(weather_data)
        
        self.color_array.clear()
        
        temp = weather_data['temperature']
        description = weather_data['shortForecast']

        self.color_array.print_text(f"Wind: {weather_data['windSpeed']}", 1, 37, [255, 255, 255])
        self.color_array.print_text(f"h%: {weather_data['relativeHumidity']}", 1, 46, [15, 189, 255])
        self.color_array.print_text(f"FL: {weather_data['perceivedTemperature']}", 1, 55, [255, 255, 50])

        self.color_array.draw_wind_dir(30, 37, weather_data['windDegree'])

        if temp < 50:
            self.color_array.print_text(f"Temp: {round(temp, 1)}", 1, 0, [0, 0, 255])
        elif temp < 78:
            self.color_array.print_text(f"Temp: {round(temp, 1)}", 1, 0, [0, 255, 0])
        else:
            self.color_array.print_text(f"Temp: {round(temp, 1)}", 1, 0, [255, 0, 0])
        
        if 'rain' in description.lower():
            precip_amount = 0 # weather_data.get('rain', {}).get('1h', 0)
            self.color_array.print_text(f"Rain: {precip_amount}mm", 0, 8, [0, 0, 255])  
            self.color_array.display_icon("rain_icon", 0, 25) 

        elif 'snow' in description.lower():
            precip_amount = 0 # weather_data.get('snow', {}).get('1h', 0)
            self.color_array.print_text(f"Snow: {precip_amount}mm", 1, 8, [255, 255, 255]) 
            self.color_array.display_icon("snow_icon", 5, 18)

        elif 'cloud' in description.lower():
            self.color_array.print_text("Cloudy", 1, 8, [128, 128, 128])  
            self.color_array.display_icon("cloud_icon", 5, 23)  
        else:
            self.color_array.print_text("Clear Sky", 1, 8, [255, 165, 0])  
            self.color_array.display_icon("sun_icon", 26, 20)

        # alerts = self.weather_request.get_alerts()
        # if alerts:
        #     self.color_array.print_text(f"Alerts: {len(alerts)}", 0, 16, [255, 0, 0])
            # self.color_array.print_text(alerts['event'], 1, 8, [255, 0, 0])
            # self.color_array.print_text(alerts['severity'], 1, 16, [255, 0, 0])
            # self.color_array.print_text(f"Expires: {alerts['expires']}", 1, 24, [255, 0, 0])

    def time(self):
        self.color_array.clear()
        self.color_array.draw_clock()

    def pool(self):
        self.color_array.clear()
        self.color_array.draw_color_array(0, 0, POOL_ART)

        data = self.pool_request.get_data()

        self.color_array.print_text(f"Pool: {data['pool']}", 2, 35, [200, 200, 255])
        self.color_array.print_text(f"{data['air']} :Air", 2, 44, [255, 200, 200])
        self.color_array.print_text(f"C: {data['count']}", 2, 54, [200, 255, 200])


if __name__ == '__main__':
    api = MatrixAPI()
    api.app.run(debug=True, host='0.0.0.0', port=5000)
