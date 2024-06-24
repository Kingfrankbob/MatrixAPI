import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_connection_manager
import adafruit_requests as adafruit_requests
from adafruit_matrixportal.graphics import Graphics
from os import getenv
from customimage import CustomImage

YOUR_API_URL = "http://192.168.1.106:5000/api/frame"

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

width = 64
height = 64
total_colors=400

graphics = Graphics(default_bg = 0x000000, bit_depth=2, width=width, height=height, alt_addr_pins=None, color_order="RGB", serpentine=True, tile_rows=1, rotation=0, debug=False)
image = CustomImage(width, height, total_colors)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
    except ConnectionError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, 'utf-8'), "\tRSSI:", esp.rssi)

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
requests = adafruit_requests.Session(pool, ssl_context)

def set_animation_frame(frame_type):
    url = YOUR_API_URL
    data = {'type': frame_type}
    try:
        response = requests.post(url, json=data)
        print(f"Fetched animation frame for {frame_type}:", response.json())
        response.close()
    except Exception as e:
        print("Error fetching animation frame:", e)


def get_animation_frame():
    url = YOUR_API_URL
    print("Fetching animation frame...") 

    try:
        for i in range(64):
            retry = 0
            while True:
                try:
                    response = requests.get(url + f"?index={i}")
                    json = response.json()
                    frame = json['frame']
                    image.set_row(i, frame)
                    response.close()
                    break
                except Exception:
                    print("Retrying...") 
                    retry += 1
                    if retry > 5: 
                        esp.connect_AP(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
                    if retry > 6: 
                        print("Failed to fetch frame cos high retry")
                        break
                    continue
        print("Finished fetching")
        # return frame 
    except Exception as e:
        print("Error fetching animation frame:", e)
        # return None

current_screen = "time" 
last_screen_change = time.monotonic()
last_time_update = time.monotonic()

screen_change_interval = 5 * 60
time_update_interval = 60 
set_animation_frame(current_screen)
get_animation_frame()
graphics._bg_group.append(image.get_group())

while True:
    now = time.monotonic()

    if now - last_time_update >= time_update_interval:
        get_animation_frame()
        graphics._bg_group.append(image.get_group())
        last_time_update = now

    if now - last_screen_change >= screen_change_interval:
        if current_screen == "time":
            current_screen = "pool"
        elif current_screen == "pool":
            current_screen = "weather"
        elif current_screen == "weather":
            current_screen = "time"  # Go back to time
        
        set_animation_frame(current_screen)
        last_screen_change = now
        get_animation_frame()
        graphics._bg_group.append(image.get_group())

    time.sleep(1)
