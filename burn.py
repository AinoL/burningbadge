from st3m.reactor import Responder
import st3m.run
from ctx import Context

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

class Example(Responder):
    def __init__(self) -> None:
        pass

    def draw(self, ctx: Context) -> None:
        ctx.image(
                "/flash/sys/apps/burningbadge/Exploits.png",
                -121,
                -121,
                242,
                242
            )

    def think(self, ins: InputState, delta_ms: int) -> None:
        pass

st3m.run.run_responder(Example())
