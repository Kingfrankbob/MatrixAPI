import gc
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
print(f"Initial Memory: {gc.mem_free()}")

# YOUR_API_URL = "http://192.168.1.106:5000/api" # my house
YOUR_API_URL = "http://192.168.10.199:5000/api" # marks house


esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, {'ssid': getenv('CIRCUITPY_WIFI_SSID'), 'password': getenv('CIRCUITPY_WIFI_PASSWORD')}, status_light)

# print("Connecting to AP...")
# while not esp.is_connected:
#     try:
#         esp.connect_AP(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
#     except ConnectionError as e:
#         print("could not connect to AP, retrying: ", e)
#         continue
# print("Connected to", str(esp.ssid, 'utf-8'), "\tRSSI:", esp.rssi)

# pool = adafruit_connection_manager.get_radio_socketpool(esp)
# ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
# wifi = adafruit_requests.Session(pool, ssl_context)

# test = wifi.get(YOUR_API_URL.replace("/api", "/api/setframe?type=wfc"))
# print(test.json())

width = 64
height = 64
total_colors=400

graphics = Graphics(default_bg = 0x000000, bit_depth=2, width=width, height=height, alt_addr_pins=None, color_order="RGB", serpentine=True, tile_rows=1, rotation=0, debug=False)
image = CustomImage(width, height, total_colors)

previouss = None

class AnimationRenderer:
    def __init__(self, url):
        self.url = url
        self.animation_array_1 = []
        self.animation_array_2 = []
        self.index = 0
        self.errors = []
    
    async def get_frame(self, index):
        json = None
        retries = 0
        while json is None:
            try:
                response = wifi.get(self.url + f"?index={self.index}")
                json = response.json()
                response.close()
            except Exception as e:
                print(f"Error fetching animation WFC frame {e}")
                retries += 1
                if retries > 6:
                    break
         
        if index == 0:
            try:
                self.animation_array_1 = json['frame']
            except Exception as e:
                self.errors.append(index)
                self.animation_array_1 = []
        else:
            try:
                self.animation_array_2 = json['frame']
            except Exception as e:
                self.errors.append(index)
                self.animation_array_2 = []
        self.index += 1
        del json
        if retries > 6:
            del response
        del retries
        gc.collect()
        return
    
    async def render_frame(self, index):
        if index == 0:
            print(f"Length = {len(self.animation_array_1)}")
            for i in range(len(self.animation_array_1)):
                element = self.animation_array_1.pop(0)
                image.set_pixel(element['x'], element['y'], element['color'])
                render_frame()
                del element
                gc.collect()

        else:
            print(f"Length = {len(self.animation_array_2)}")
            for i in range(len(self.animation_array_2)):
                element = self.animation_array_2.pop(0)
                image.set_pixel(element['x'], element['y'], element['color'])
                render_frame()
                del element
                gc.collect()
    
    async def render_wfc(self):
        image.clear()
        gc.collect()
        
        await self.get_frame(0)
        
        for i in range(1, 64):
            gc.collect()
            await self.render_frame((i - 1) % 2)
            await self.get_frame(i % 2)
            render_frame()
            print(gc.mem_free())

        await self.render_frame(1)
        # print("Finished, Errors:", self.errors) 

        for i in range(len(self.errors)):
            error = self.errors.pop(0)
            await self.get_frame(error)
            await self.render_frame(error % 2)


renderer = AnimationRenderer(YOUR_API_URL + "/frame")

def set_animation_frame(frame_type, retries=6):
    url = YOUR_API_URL + "/setframe?type=" + frame_type
    retry = 0
    success = False
    response = None

    while retry <= retries:
        try:
            response = wifi.get(url)
            json_data = response.json()
            if json_data['message'] == f"Animation frame for {frame_type} set successfully":
                print(f"Successfully changed frame {frame_type}!")
                success = True
                break
            response.close()
            del response
            del json_data
        except Exception:
            retry += 1
            time.sleep(2 ** retry)

    if not success:
        print(f"Failed to set animation frame {frame_type} after {retries} retries.")
    if response is not None:
        response.close()
    del success
    del url
    del retry
    gc.collect()


def fetch_frame(url, index, retries=4):
    retry = 0
    response = None
    while retry <= retries:
        try:
            response = wifi.get(url + f"?index={index}")
            json_data = response.json()
            frame = json_data['frame']
            response.close()
            del response
            del json_data
            return frame
        except Exception as e:
            print(f"Error fetching frame {e}")
            if response is not None:
                response.close()
                del response
            retry += 1
            if retry > retries:
                return None
            gc.collect()
            time.sleep(2 ** retry)

def get_animation_frame():
    errors = []
    url = YOUR_API_URL + "/frame"
    gc.collect()
    image.clear()

    if current_screen in ["time", "pool", "weather"]:
        for i in range(64):
            print(f"On Row {i}")
            frame = fetch_frame(url, i)
            if frame:
                image.set_row(i, frame)
                del frame
            else:
                errors.append(i)

        for error_index in errors:
            frame = fetch_frame(url, error_index)
            if frame:
                image.set_row(error_index, frame)
                del frame

        del errors
        gc.collect()
    else:
        asyncio.run(render_wfc())

    gc.collect()

async def render_wfc():
    gc.collect()
    await asyncio.sleep(10)
    asyncio.run(renderer.render_wfc())
        
def render_frame():
    graphics.splash.append(image.get_group())
    for i in range(len(graphics.splash) - 1):
        graphics.splash.pop(0)
    gc.collect()

current_screen = "time"
# last_screen_change = time.monotonic()
# last_time_update = time.monotonic() - 60 

# screen_change_interval = 5 * 60
# time_update_interval = 60 

# test_get = wifi.get(YOUR_API_URL)

# print(test_get.json())

set_animation_frame(current_screen)
get_animation_frame()
render_frame()

while True: 
    pass 


# while True:
#     now = time.monotonic()

#     if now - last_time_update >= time_update_interval:
#         get_animation_frame()
#         render_frame()
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
#         render_frame()


#     time.sleep(1)
