import time
from raspi.HD44780.HD44780 import HD44780
import psutil
from flask import Flask, request, jsonify
from flask_restful import Api
from matrixscreen.matrix import LEDMatrix
from noaaWeatherApi import NOAAWeather
from pool import POOL_ART, pool_data
from hilbertcurve.hilbertHandler import HilbertHandler
from wavefunctioncollapse.wfcRender import WFCRender
from moon.moon import MoonRender
from random import randint
import logging
import datetime
import pytz
import socket

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MatrixAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.setup_API_rules()

        self.types = ['weather', 'pool', 'time', 'wfc', 'hilbert', 'moon']
        self.width = 64
        self.height = 64
        self.current_screen = self.types[2]
        self.index = 0
        self.generating = False

        self.color_array = LEDMatrix(self.width, self.height)

        self.lcd = [
            HD44780(40, 2, 5, 6, 13, 19, -1, -1, -1, -1, 16, 20),
            HD44780(40, 2, 5, 6, 13, 19, -1, -1, -1, -1, 16, 21)
        ]

        self.last_request = ""

        self.setup_data()
        self.update_screen()
        self.screensaver = None
        self.memsave = False



    def setup_API_rules(self):
        self.app.add_url_rule('/', 'hello_world', self.hello_world)
        self.app.add_url_rule('/api/frame', 'get_anim_frame', self.get_anim_frame, methods=['GET'])
        self.app.add_url_rule('/api/setframe', 'set_anim_frame', self.set_anim_frame, methods=['GET'])
        self.app.add_url_rule('/api/wfc', 'redo_wfc', self.redo_wfc, methods=['GET'])
        self.app.add_url_rule('/api/checkmoon', 'check_moon', self.check_moon, methods=['GET'])
        self.app.add_url_rule('/api/works', 'api_works', self.api_works, methods=['GET'])
        self.app.add_url_rule('/api/savescreen', 'save_screen_from_mem', self.save_screen_from_mem, methods=['GET'])
        self.app.add_url_rule('/api/checkscreen', 'load_screen_from_mem', self.load_screen_from_mem, methods=['GET'])
        self.app.after_request(self.log_request)

    def setup_data(self):
        self.weather_request = NOAAWeather()
        self.pool_request = pool_data()
        self.wfc = WFCRender()
        self.hilbert = HilbertHandler(randint(4, 5), randint(0, 2))
        self.moon = MoonRender(self.weather_request)

    def log_request(self, response):
        self.last_request = f"{request.method} {request.url[17:]}"
        self.update_lcd()
        return response

    def update_screen(self):
        logging.info("Updating screen: " + self.current_screen)
        if self.current_screen == "weather":
            self.weather()
        elif self.current_screen == "time":
            self.time()
        elif self.current_screen == "pool":
            self.pool()
        elif self.current_screen == "wfc":
            self.wavefuncllaps()
        elif self.current_screen == "hilbert":
            self.hilbert_curve()
        elif self.current_screen == "moon":
            self.moon_phase()
        self.update_lcd()

    def weather(self):
        weather_data = self.weather_request.get_weather()
        if 'error' in weather_data:
            logging.error(weather_data['error'])
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

        if 'rain' in description.lower() or 'showers' in description.lower() or 'thunder' in description.lower() \
            or 'drizzle' in description.lower() or 'sleet' in description.lower():
            precip_amount = 0
            self.color_array.print_text(f"Rain: {precip_amount}mm", 0, 8, [0, 0, 255])
            self.color_array.display_icon("rain_icon", 0, 25)

        elif 'snow' in description.lower():
            precip_amount = 0
            self.color_array.print_text(f"Snow: {precip_amount}mm", 1, 8, [255, 255, 255])
            self.color_array.display_icon("snow_icon", 5, 18)

        elif 'cloud' in description.lower():
            self.color_array.print_text("Cloudy", 1, 8, [128, 128, 128])
            self.color_array.display_icon("cloud_icon", 5, 23)
        else:
            self.color_array.print_text("Clear Sky", 1, 8, [255, 165, 0])
            self.color_array.display_icon("sun_icon", 26, 20)

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

    def wavefuncllaps(self):
        self.color_array.clear()
        self.wfc = WFCRender()
        self.wfc.start_wfc()
        self.generating = False

    def hilbert_curve(self):
        self.color_array.clear()
        self.hilbert = HilbertHandler(randint(4, 5), randint(0, 2))
        self.hilbert.render()

    def hello_world(self):
        return jsonify({'test': "This is Michael's API, feel free to ask for help on the API. However im more curious why your even here"}), 200

    def get_anim_frame(self):
        try:
            index = request.args.get('index', type=int)
        except ValueError as e:
            logging.error("Index must be an integer")
            return jsonify({'message': 'Index must be an integer'}), 400
        if self.current_screen == "wfc":
            try:
                elements = self.wfc.get_elements(index)
                return jsonify({'frame': elements}), 200
            except IndexError as e:
                logging.error("Index out of range for wfc")
                return jsonify({'message': 'Index out of range for wfc'}), 400
        elif self.current_screen == "hilbert":
            try:
                current_frame = self.hilbert.get_elements(index)
                return jsonify({'frame': current_frame}), 200
            except IndexError as e:
                logging.error("Index out of range for hilbert")
                return jsonify({'message': 'Index out of range for hilbert'}), 400
        else:
            try:
                current_frame = self.color_array.matrix[index]
                return jsonify({'frame': current_frame}), 200
            except IndexError as e:
                logging.error("Index out of range for current screen")
                return jsonify({'message': 'Index out of range for current screen'}), 400

    def redo_wfc(self):
        try:
            self.current_screen = "wfc"
            self.wfc.start_wfc()
            return jsonify({'message': 'WFC Redone'}), 200
        except Exception as e:
            logging.error("Error redoing WFC")
            return jsonify({'message': 'Error redoing WFC'}), 400

    def set_anim_frame(self):
        screenType = request.args.get('type', type=str)

        current_hour = datetime.datetime.now(pytz.timezone('America/Chicago')).hour
        if (current_hour > 20 or current_hour < 6):
            if self.current_screen != "moon":
                self.current_screen = "moon"
                self.update_screen()
            return jsonify({'message': 'Cannot set screen during moon phase time'}), 403

        if screenType not in self.types:
            logging.error("Animation type is not valid")
            return jsonify({'message': 'Animation type is not valid'}), 400
        self.current_screen = screenType
        self.update_screen()
        return jsonify({'message': f'Animation frame for {screenType} set successfully'}), 200

    def moon_phase(self):
        self.color_array.clear()
        logging.info("Showing moon phase")
        self.color_array.draw_color_array(0, 0, self.moon.get_moon_phase())

    def check_moon(self):
        current_hour = datetime.datetime.now(pytz.timezone('America/Chicago')).hour
        if (current_hour > 20 or current_hour < 6):
            if self.current_screen != "moon":
                self.current_screen = "moon"
                self.update_screen()
            return jsonify({'message': 'Its time to show the moon!'}), 403
        return jsonify({'message': 'Not time for the moon yet!'}), 200

    def api_works(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({
            'status': 'API is running',
            'current_screen': self.current_screen,
            'current_time': current_time
        }), 200

    def save_screen_from_mem(self):
        screenTypes = request.args.get('remaining')
        if screenTypes is None:
            return jsonify({'message': 'No screen types provided'}), 400
        print("Screen types", screenTypes)
        self.screensaver = screenTypes
        self.memsave = True
        return jsonify({'message': 'Screen saved to memory'}), 200

    def load_screen_from_mem(self):
        if self.screensaver is None or not self.memsave:
            return jsonify({'message': 'No screen types saved in memory'}), 201
        self.memsave = False
        return {'message': 'Screen loaded from memory', 'screen': self.current_screen, 'remaining': self.screensaver}, 200

    def update_lcd(self):
        """
        Updates the 4x40 LCD screen with the latest information.
        """
        def whitespace(length):
            return ' ' * length

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.used / (1024 ** 3)  # Convert to GB
        total_memory = memory_info.total / (1024 ** 3)  # Convert to GB

        self.lcd[0].set_cursor(0, 0)
        stri = f"{self.last_request}"
        length = len(stri)
        buffer = (int)((40 - length) / 2)
        self.lcd[0].text(f"{whitespace(buffer)}{stri}{whitespace(buffer)}  ".encode('utf-8'))

        self.lcd[0].set_cursor(0, 1)
        stri = f"CPU: {cpu_usage}% Mem: {memory_usage:.1f}/{total_memory:.1f}GB"
        length = len(stri)
        buffer = (int)((40 - length) / 2)
        self.lcd[0].text(f"{whitespace(buffer)}{stri}{whitespace(buffer)}  ".encode('utf-8'))

        self.lcd[1].set_cursor(0, 0)
        stri = "Static IP: 192.168.1.200/11"
        length = len(stri)
        buffer = (int)((40 - length) / 2)
        self.lcd[1].text(f"{whitespace(buffer)}{stri}{whitespace(buffer)}  ".encode('utf-8'))

        self.lcd[1].set_cursor(0, 1)
        stri = f"{now} Screen: {self.current_screen}"
        length = len(stri)
        buffer = (int)((40 - length) / 2)
        self.lcd[1].text(f"{whitespace(buffer)}{stri}{whitespace(buffer)}  ".encode('utf-8'))


if __name__ == '__main__':
    api = MatrixAPI()
    api.app.run(debug=True, host='0.0.0.0', port=5000)