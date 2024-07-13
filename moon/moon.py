from .moonArt import NEW_MOON, FULL_MOON, FIRST_QUARTER, WANING_CRESCENT, WANING_GIBBOUS, WAXING_CRESCENT, WAXING_GIBBOUS, THIRD_QUARTER
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MoonRender:
    def __init__(self, weather) -> None:
        self.weather = weather

    def get_moon_phase(self):
        moon_phase = self.weather.get_moon_phase()['phase']

        if "New Moon" in moon_phase:
            return NEW_MOON
        elif "First Quarter" in moon_phase:
            return FIRST_QUARTER
        elif "Full Moon" in moon_phase:
            return FULL_MOON
        elif "Waning Crescent" in moon_phase:
            return WANING_CRESCENT
        elif "Waning Gibbous" in moon_phase:
            return WANING_GIBBOUS
        elif "Waxing Crescent" in moon_phase:
            return WAXING_CRESCENT
        elif "Waxing Gibbous" in moon_phase:
            return WAXING_GIBBOUS
        elif "Last Quarter" in moon_phase or "Third Quarter" in moon_phase:
            return THIRD_QUARTER
        else:
            logging.exception(f"Unknown moon phase: {moon_phase}")
    
if "__name__" == "__main__":
    moon = MoonRender()
    moon.get_moon_phase()

        
