from flask import Flask, request, jsonify
from flask_restful import Api
from matrix import LEDMatrix
from noaaWeatherApi import NOAAWeather
from pool import POOL_ART, pool_data
from hilbert_curve import HilbertHandler
from wfcMCEdition import WFCRender
from random import randint

types = ['weather', 'pool', 'time', 'wfc', 'hilbert']

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
        self.wfc = WFCRender()
        self.hilbert = HilbertHandler()
        self.generating = False

        self.update_screen()
        
        self.app.add_url_rule('/', 'hello_world', self.hello_world)
        self.app.add_url_rule('/api/frame', 'get_anim_frame', self.get_anim_frame, methods=['GET'])
        self.app.add_url_rule('/api/setframe', 'set_anim_frame', self.set_anim_frame, methods=['GET'])
        self.app.add_url_rule('/api/wfc', 'redo_wfc', self.redo_wfc, methods=['GET'])

    def hello_world(self):
        return jsonify({'test': "This is Michael's API, feel free to ask for help on the API. However im more curious why your even here"}), 200
        
    def get_anim_frame(self):
        index = request.args.get('index', type=int)
        if self.current_screen == "wfc":
            elements = self.wfc.get_elements(index)
            return {'frame': elements}, 200 
        elif self.current_screen == "hilbert":
            current_frame = self.hilbert.get_frame(index)
            return {'frame': current_frame}, 200
        try:
            current_frame = self.color_array.matrix[index]
            return {'frame': current_frame}, 200
        except IndexError as e:
            return {'message': 'Index out of range'}, 400
        
    def redo_wfc(self):
        self.current_screen = "wfc"
        self.wfc.start_wfc()
        return jsonify({'message': 'WFC Redone'}), 200

    def set_anim_frame(self):
        typee = request.args.get('type', type=str)
        if typee not in types:
            return jsonify({'message': f'Animation is not valid'}), 400
        self.current_screen = typee
        self.update_screen()
        return jsonify({'message': f'Animation frame for {typee} set successfully'}), 200


    def update_screen(self):
        print("Updating screen: " + self.current_screen)
        if self.current_screen == "weather":
            self.weather()
        elif self.current_screen == "time":
            self.time()
        elif self.current_screen == "pool":
            self.pool()
        elif self.current_screen == "wfc":
            self.wave()
        elif self.current_screen == "hilbert":
            self.hilbert()


    def wave(self):
        self.color_array.clear()
        self.wfc = WFCRender()
        self.wfc.start_wfc()
        self.generating = False


    def weather(self):
        weather_data = self.weather_request.get_weather()
        if 'error' in weather_data:
            return
                
        self.color_array.clear()
        
        temp = weather_data['temperature']
        description = weather_data['shortForecast']

        self.color_array.print_text(f"Wind: {weather_data['windSpeed']}", 1, 37, [255, 255, 255])
        self.color_array.print_text(f"h%: {weather_data['relativeHumidity']}", 1, 46, [15, 189, 255])
        self.color_array.print_text(f"FL:{weather_data['perceivedTemperature']}", 1, 55, [255, 255, 50])

        self.color_array.draw_wind_dir(38, 37, weather_data['windDegree'])

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

    def hilbert(self):
        self.color_array.clear()
        self.hilbert = HilbertHandler(randint(4, 5), randint(0, 2))
        self.hilbert.render()


if __name__ == '__main__':
    api = MatrixAPI()
    api.app.run(debug=True, host='0.0.0.0', port=5000)
