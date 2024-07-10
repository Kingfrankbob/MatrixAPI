import gc

class AnimationRenderer:
    def __init__(self, url, animation_type, graphics, wifi, image):
        self.url = url
        self.animation_type = animation_type
        self.animation_array_1 = []
        self.animation_array_2 = []
        self.index = 0
        self.errors = []
        self.graphics = graphics
        self.image = image
        self.wifi = wifi
    
    async def get_frame(self, index):
        json = None
        retries = 0
        response = None
        while json is None:
            try:
                response = self.wifi.get(self.url + f"?index={self.index}")
                json = response.json()
                response.close()
            except Exception as e:
                print(f"Error fetching animation {self.animation_type} frame {e}")
                if response is not None:
                    response.close()
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
        del response
        del retries
        gc.collect()
        return
    
    async def render_frame(self, index):
        if self.animation_type == "hilbert":
            await self._render_hilbert_frame(index)
        else:
            await self._render_wfc_frame(index)
    
    async def _render_wfc_frame(self, index):
        if index == 0:
            print(f"Length = {len(self.animation_array_1)}")
            for i in range(len(self.animation_array_1)):
                element = self.animation_array_1.pop(0)
                self.image.set_pixel(element['x'], element['y'], element['color'])
                self.render_current_frame()
                del element
                gc.collect()

        else:
            print(f"Length = {len(self.animation_array_2)}")
            for i in range(len(self.animation_array_2)):
                element = self.animation_array_2.pop(0)
                self.image.set_pixel(element['x'], element['y'], element['color'])
                self.render_current_frame()
                del element
                gc.collect()
    
    async def _render_hilbert_frame(self, index):
        # add an error catch incase we are missing some data from the server ex: missing elements
        if index == 0:
            print(f"Length = {len(self.animation_array_1)}")
            for i in range(len(self.animation_array_1)):
                element = self.animation_array_1.pop(0)
                self.image.draw_line(element['x1'], element['y1'], element['x2'], element['y2'], element['color'])
                self.render_current_frame()
                del element
                gc.collect()

        else:
            print(f"Length = {len(self.animation_array_2)}")
            for i in range(len(self.animation_array_2)):
                element = self.animation_array_2.pop(0)
                self.image.draw_line(element['x1'], element['y1'], element['x2'], element['y2'], element['color'])
                self.render_current_frame()
                del element
                gc.collect()
    
    async def render_animation(self):
        self.image.clear()
        gc.collect()

        frame_count = 64
        if self.animation_type == "hilbert":
            frame_count = 32
            self.image.set_color_amount(1100)
        
        await self.get_frame(0)
        
        for i in range(1, frame_count):
            gc.collect()
            await self.render_frame((i - 1) % 2)
            await self.get_frame(i % 2)
            self.render_current_frame()
            print(gc.mem_free())

        await self.render_frame(1)

        print("Errors: ", self.errors)

        for i in range(len(self.errors)):
            error = self.errors.pop(0)
            await self.get_frame(error)
            await self.render_frame(error % 2)

    def render_current_frame(self):
        self.graphics.splash.append(self.image.get_group())
        for i in range(len(self.graphics.splash) - 1):
            self.graphics.splash.pop(0)
        gc.collect()
