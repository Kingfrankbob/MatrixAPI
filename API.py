from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from matrix import LEDMatrix
from weather import weather

class matrix_api:
    app = Flask(__name__)

    def __init__(self):
        self.width = 64
        self.height = 64
        self.color_array = LEDMatrix(self.width, self.height)
        self.current_screen = "weather"
        self.weather_request = weather()

    @app.route('/', methods=['GET'])
    def hello_world(self):
            return jsonify({'test': 'This is Michael\'s API, feel free to ask for help on the \nHowever im more curious why your even here'}), 200
        
    @app.route('/api/frame', methods=['GET'])
    def get_anim_frame(self):
        return jsonify({'frame': self.color_array.matrix}), 200

    @app.route('/api/frame', methods=['POST'])
    def set_anim_frame(self):
        data = request.get_json()
        self.current_screen = data.get('type')
        self.update_screen()
        return jsonify({'message': f'Animation frame for {data.get('type')} set successfully'}), 200 

    def update_screen(self):
        if(self.current_screen == "weather"):
            self.weather()
        elif(self.current_screen == "time"):
            self.time()
        elif(self.current_screen == "pool"):
            self.pool()

        pass

    def weather(self):
        weather_data = self.weather_request.get_weather_json()['data']
        if 'error' in weather_data:
            return
        
        self.color_array.clear()
        
        temp = (weather_data['main']['temp'] * 1.8) + 32# 
        description = weather_data['weather'][0]['description']
        clouds = weather_data['clouds']['all']

        self.color_array.print_text(f"Wind:{weather_data['wind']['speed']}m/s", 1, 37, [255, 255, 255])
        self.color_array.print_text(f"h%:{weather_data['main']['humidity']}", 1, 46, [200, 225, 255])
        self.color_array.print_text(f"FL:{round(weather_data['main']['feels_like'])}", 1, 55, [255, 255, 255])

        self.color_array.draw_wind_dir(30, 37, weather_data['wind']['deg'])

        if(temp < 50):
            self.color_array.print_text(f"Temp: {round(temp, 1)}", 1, 0, [0, 0, 255])
        elif(temp < 78):
            self.color_array.print_text(f"Temp: {round(temp, 1)}", 1, 0, [0, 255, 0])
        else:
            self.color_array.print_text(f"Temp: {round(temp, 1)}", 1, 0, [255, 0, 0])
        
        if 'rain' in description.lower():
            precip_amount = weather_data.get('rain', {}).get('1h', 0)
            self.color_array.print_text(f"Rain: {precip_amount}mm", 0, 8, [0, 0, 255])  
            self.color_array.display_icon("rain_icon", 0, 25) 

        elif 'snow' in description.lower():
            precip_amount = weather_data.get('snow', {}).get('1h', 0)
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
        self.color_array.draw_clock(0, 0)

    def pool(self):
        pass


if __name__ == '__main__':
    # matrix_api.app.run(debug=True)
    matrix_apii = matrix_api()
    matrix_apii.time()
    matrix_apii.color_array.print()