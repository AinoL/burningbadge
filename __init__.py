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
            [250, 192, 0]
        ]
        self.i = 0
        self.time = 0
        
    def draw(self, ctx: Context) -> None:
        if self.i == 0:
            ctx.image(
                "/flash/sys/apps/cccflower/Exploits.png",
                -121,
                -121,
                242,
                242
            )
        self.time = (self.time + 1)%10
        if self.time == 0:
            for f in self.fire_array:
                leds.set_rgb(self.i, *f)
                self.i = (self.i + 1)%40
            c = self.fire_array.pop(0)
            self.fire_array.append(c)
            leds.update()

    def think(self, ins: InputState, delta_ms: int) -> None:
        pass

if __name__ == "__main__":
    st3m.run.run_view(Burn(ApplicationContext()))
