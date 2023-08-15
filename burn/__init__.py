from st3m.application import Application, ApplicationContext
from st3m.reactor import Responder
import st3m.run
import leds
import random

class Burn(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        leds.set_slew_rate(4)
        random.seed()

    def draw(self, ctx: Context) -> None:
        # Paint the background black
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()

        ctx.rgb(255, 255, 255)
        ctx.font = "Camp Font 3"

        text = "burn1ngfl0w3rs"
        w = ctx.text_width(text)
        ctx.move_to(-w/2, -20)
        ctx.text(text)

        text = "tv"
        w = ctx.text_width(text)
        ctx.move_to(-w/2, 20)
        ctx.text(text)

        for i in range(40):
            leds.set_rgb(
                i,
                random.randint(50, 255)/255,
                random.randint(10, 60)/255,
                0
            )
        leds.update()

    def think(self, ins: InputState, delta_ms: int) -> None:
        pass

if __name__ == "__main__":
    st3m.run.run_view(Burn(ApplicationContext()))
