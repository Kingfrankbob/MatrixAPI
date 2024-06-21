from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from matrix import LEDMatrix
from weather import weather

class matrix_api:
    app = Flask(__name__)
    # api = API(app)

    def __init__(self):
        self.width = 64
        self.height = 64
        self.color_array = LEDMatrix(self.width, self.height)
        self.current_screen = "weather"
        self.weather_request = weather()

    @app.route('/', methods=['GET'])
    def hello_world(self):
            return jsonify({'hello': 'world'}), 200
        
    @app.route('/frame', methods=['GET'])
    def get_anim_frame(self):
        return jsonify({'frame': self.color_array.matrix}), 200

    @app.route('/frame', methods=['POST'])
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
        weather_data = get_weather_json()
        if 'error' in weather_data:
            return

        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        clouds = weather_data['clouds']['all']
        
        self.color_array.print_text(f"Temp: {temp}°C", 0, 0, [0, 255, 0])

        if 'rain' in description.lower():
            precip_amount = weather_data.get('rain', {}).get('1h', 0)
            self.color_array.print_text(f"Rain: {precip_amount}mm", 0, 20, [0, 0, 255])  
            self.color_array.display_icon("rain_icon", 30, 20) 

        elif 'snow' in description.lower():
            precip_amount = weather_data.get('snow', {}).get('1h', 0)
            self.color_array.print_text(f"Snow: {precip_amount}mm", 0, 20, [255, 255, 255]) 
            self.color_array.display_icon("snow_icon", 30, 20)

        elif 'cloud' in description.lower():
            self.color_array.print_text("Cloudy", 0, 20, [128, 128, 128])  
            self.color_array.display_icon("cloud_icon", 30, 20)  

        else:
            self.color_array.print_text("Clear Sky", 0, 20, [255, 165, 0])  
            self.color_array.display_icon("sun_icon", 30, 20) 

    def time(self):
        pass

    def pool(self):
        pass


if __name__ == '__main__':
    # matrix_api.app.run(debug=True)
    matrix_apii = matrix_api()
    matrix_apii.weather()
    matrix_apii.color_array.print()