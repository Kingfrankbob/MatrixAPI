from flask import Flask, request, jsonify
from flask_restful import Resource, API
from .matrix import LEDMatrix
from .weather import get_weather_json

app = Flask(__name__)
api = API(app)

width = 64
height = 64
color_array = LEDMatrix(width, height)
current_screen = "weather"

@app.route('/', methods=['GET'])
def hello_world():
        return jsonify({'hello': 'world'}), 200
    
@app.route('/frame', methods=['GET'])
def get_anim_frame():
    global color_array
    return jsonify({'frame': color_array.matrix}), 200

@app.route('/frame', methods=['POST'])
def set_anim_frame():
    global current_screen
    data = request.get_json()
    current_screen = data.get('type')
    update_screen()
    
    return jsonify({'message': f'Animation frame for {data.get('type')} set successfully'}), 200 

def update_screen():
     
    global current_screen

    if(current_screen == "weather"):
        weather()
    elif(current_screen == "time"):
        time()
    elif(current_screen == "pool"):
        pool()

    pass

def weather():
    weather_data = get_weather_json()
    if 'error' in weather_data:
          return
    
    global color_array

    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    clouds = weather_data['clouds']['all']
    
    color_array.print_text(f"Temp: {temp}°C", 0, 0, [0, 255, 0])

    if 'rain' in description.lower():
        precip_amount = weather_data.get('rain', {}).get('1h', 0)
        LEDMatrix.print_text(f"Rain: {precip_amount}mm", 0, 20, [0, 0, 255])  
        LEDMatrix.display_icon("rain_icon", 30, 20) 

    elif 'snow' in description.lower():
        precip_amount = weather_data.get('snow', {}).get('1h', 0)
        LEDMatrix.print_text(f"Snow: {precip_amount}mm", 0, 20, [255, 255, 255]) 
        LEDMatrix.display_icon("snow_icon", 30, 20)

    elif 'cloud' in description.lower():
        LEDMatrix.print_text("Cloudy", 0, 20, [128, 128, 128])  
        LEDMatrix.display_icon("cloud_icon", 30, 20)  

    else:
        LEDMatrix.print_text("Clear Sky", 0, 20, [255, 165, 0])  
        LEDMatrix.display_icon("sun_icon", 30, 20) 

    pass

def time():
     pass

def pool():
     pass


if __name__ == '__main__':
    app.run(debug=True)