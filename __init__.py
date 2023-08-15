from st3m.application import Application, ApplicationContext
from st3m.reactor import Responder
import st3m.run
import leds
import random
import time

class Burn(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        random.seed()
        leds.set_slew_rate(10)
        self.fire_array = [
            [128, 17, 0],
            [182, 34, 3],
            [215, 53, 2],
            [252, 100, 0],
            [255, 117, 0],
            [250, 170, 0]
        ]
        self.i = 0
        self.time = 0

        self.led_buffer = [[0, 0,0]]*40
        self.last_draw = 0
        self.interval = 250
        
    def draw(self, ctx: Context) -> None:
        ctx.image(
            "/flash/sys/apps/cccflower/Exploits.png",
            -121,
            -121,
            242,
            242
        )

        for i, led in enumerate(self.led_buffer):
            leds.set_rgb(i, *led)

        leds.update()

    def think(self, ins: InputState, delta_ms: int) -> None:
        self.last_draw += delta_ms

        rage = 500 * (delta_ms / 1000)

        direction = ins.buttons.app # -1 (left), 1 (right), or 2 (pressed)
        if direction == -1 and self.interval < 1000:
            self.interval += rage

        elif direction == 1 and self.interval > 30:
            self.interval -= rage


        if self.last_draw < self.interval:
            return

        self.last_draw = 0

        for f in self.fire_array:
            self.led_buffer[self.i] = f
            self.i = (self.i + 1) % 40

        c = self.fire_array.pop(0)
        self.fire_array.append(c)

if __name__ == "__main__":
    st3m.run.run_view(Burn(ApplicationContext()))
