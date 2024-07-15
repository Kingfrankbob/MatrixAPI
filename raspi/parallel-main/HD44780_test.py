
import time

from HD44780 import HD44780

# initialize the chips
lcd=[]
lcd.append(HD44780(40, 2, 5, 6, 13, 19, -1, -1, -1, -1, 16, 20))
lcd.append(HD44780(40, 2, 5, 6, 13, 19, -1, -1, -1, -1, 16, 21))

# times and euro characters (positions 0 and 1)



# write the first text
lcd[0].set_cursor(0,0)
lcd[0].text(b'40 4 DISPLAY        wyhygtfrew E                ')
lcd[0].set_cursor(0,1)
lcd[0].text(b'              HD44780 CHIP              ')
lcd[1].set_cursor(0,0)
lcd[1].text(b'                                        ')
lcd[1].set_cursor(0,1)
lcd[1].text(b'             Raspberry Pi 3             ')

time.sleep(10)


for i in lcd:
    i.close()