import gc
gc.collect()
print(gc.mem_free())

# data = []
# for _ in range(4096):
#     gc.collect()
#     print(gc.mem_free(), _)

#     data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
import adafruit_connection_manager
import adafruit_requests as adafruit_requests
from adafruit_matrixportal.graphics import Graphics
from os import getenv
from customimage import CustomImage
import neopixel
import asyncio

#yes 
# YOUR_API_URL = "http://192.168.1.106:5000/api/frame"
YOUR_API_URL = "http://192.168.10.195:5000/api/frame"



esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, {'ssid': getenv('CIRCUITPY_WIFI_SSID'), 'password': getenv('CIRCUITPY_WIFI_PASSWORD')}, status_light)

width = 64
height = 64
total_colors=400

graphics = Graphics(default_bg = 0x000000, bit_depth=2, width=width, height=height, alt_addr_pins=None, color_order="RGB", serpentine=True, tile_rows=1, rotation=0, debug=False)
image = CustomImage(width, height, total_colors)

class AnimationRenderer:
    def __init__(self, url):
        self.url = url
        self.animation_array_1 = []
        self.animation_array_2 = []
    
    async def get_frame(self, index):
        print("Fetching animation frame...")
        response = wifi.get(self.url)
        json = response.json()
        response.close()
        if index == 0:
            self.animation_array_1 = json['frame']
        else:
            self.animation_array_2 = json['frame']
        del json
        del response
        gc.collect()
        return
    
    async def render_frame(self, index):
        if index == 0:
            print(f"Length = {len(self.animation_array_1)}")
            for i in range(len(self.animation_array_1)):
                element = self.animation_array_1.pop(0)
                image.set_pixel(element['x'], element['y'], element['color'])
                render_frame()
                await asyncio.sleep(0.1)
                del element
                gc.collect()

        else:
            print(f"Length = {len(self.animation_array_2)}")
            for i in range(len(self.animation_array_2)):
                element = self.animation_array_2.pop(0)
                image.set_pixel(element['x'], element['y'], element['color'])
                render_frame()
                await asyncio.sleep(0.1)
                del element
                gc.collect()
        print("Finished execution for frame")
    
    async def render_wfc(self):
        print("Fetching animation WFC frame...")
        image.clear()
        gc.collect()
        
        await self.get_frame(0)
        
        for i in range(1, 64):
            print(gc.mem_free())
            await self.get_frame(i % 2)
            await self.render_frame((i - 1) % 2)
            gc.collect()
            


renderer = AnimationRenderer(YOUR_API_URL)

# Example usage:
# url = "YOUR_API_URL"
# wifi = YourWifiModule()
# image = YourImageModule()
# renderer = AnimationRenderer(url, wifi, image)
# asyncio.run(renderer.render_wfc())


def set_animation_frame(frame_type):
    url = YOUR_API_URL
    data = {'type': frame_type}
    response = wifi.post(url, json=data)
    print(f"Fetched animation frame for {frame_type}:", response.json())
    response.close()
    del url
    del data
    del response
    gc.collect()

def get_animation_frame():
    url = YOUR_API_URL
    gc.collect()
    print("Fetching animation frame...") 
    image.clear()
    if current_screen != "wfc":
        try:
            for i in range(64):
                print(f"On Row {i}")
                retry = 0
                while True:
                    try:
                        response = wifi.get(url + f"?index={i}")
                        json = response.json()
                        frame = json['frame']
                        image.set_row(i, frame)
                        response.close()
                        break 
                    except Exception:
                        retry += 1
                        if retry > 6: 
                            break
                        continue
        except Exception as e:
            print("Error fetching animation frame:", e)
    else:
        # pass
        asyncio.run(render_wfc())

async def render_wfc():
    gc.collect()
    asyncio.run(renderer.render_wfc())
        

def render_frame():
    gc.collect()
    graphics._bg_group.append(image.get_group())


current_screen = "wfc" 
# last_screen_change = time.monotonic()
# last_time_update = time.monotonic() - 60

# screen_change_interval = 5 * 60
# time_update_interval = 60 
set_animation_frame(current_screen)
get_animation_frame()



# while True:
#     now = time.monotonic()

#     if now - last_time_update >= time_update_interval:
#         get_animation_frame()
#         graphics._bg_group.append(image.get_group())
#         last_time_update = now

#     if now - last_screen_change >= screen_change_interval:
#         if current_screen == "time":
#             current_screen = "pool"
#         elif current_screen == "pool":
#             current_screen = "weather"
#         elif current_screen == "weather":
#             current_screen = "wfc"
#         elif current_screen == "wfc":
#             current_screen = "time"
        
#         set_animation_frame(current_screen)
#         last_screen_change = now
#         get_animation_frame()
#         graphics._bg_group.append(image.get_group())

#     time.sleep(1)
