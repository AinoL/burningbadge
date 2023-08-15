import leds
import time

fire_array = [
    [128, 17, 0],
    [182, 34, 3],
    [215, 53, 2],
    [252, 100, 0],
    [255, 117, 0],
    [250, 192, 0]
]

ledcounter = 0
offset = 0
while True:
    while ledcounter < 40:
        for i in fire_array:
            leds.set_rgb(ledcounter, *i)
            leds.update()
            time.sleep(0.1)
            ledcounter = ledcounter+1
    c = fire_array.pop(1)
    print(c)
    fire_array.append(c)
    ledcounter = 0
    offset = offset + 1