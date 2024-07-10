import gc

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

        for i in range(len(self.errors)):
            error = self.errors.pop(0)
            await self.get_frame(error)
            await self.render_frame(error % 2)