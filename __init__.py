from st3m.application import Application, ApplicationContext
from st3m.reactor import Responder
import st3m.run
import leds
import random
import time
import math
import json

top_left_x = math.ceil(
    120 * math.cos(
        math.radians(360-45)
    )
)
top_left_y = math.ceil(
    120 * math.sin(
        math.radians(360-45)
    )
)

bottom_right_x = math.ceil(120 * math.cos(180-45))
bottom_right_y = math.ceil(120 * math.sin(180-45))

class Burn(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)

        try:
            with open("/flash/nick.json") as f:
                data = json.load(f)
        except OSError:
            data = {}

        self.name = data.get("name", "flow3r")
        self._scale = 0
        self._phase = 0.0

        random.seed()
        leds.set_slew_rate(10)


        self.i = 0
        self.time = 0

        self.fire_array = [
            [128, 17, 0],
            [182, 34, 3],
            [215, 53, 2],
            [252, 100, 0],
            [255, 117, 0],
            [250, 170, 0]
        ]

        self.led_buffer = [self.fire_array[0]]*40
        self.led_since_step = 0
        self.led_interval = 250
        self.led_fire_array_index = 0


        self.image_since_step = 0
        self.image_interval = 10000
        self.image_index = 1
        self.burning_flower = [
                "/flash/sys/apps/cccflower/burningflowers.png",
                -top_left_x,
                top_left_y,

                math.ceil(math.fabs(top_left_x * 2)),
                math.ceil(math.fabs(top_left_y * 2)),
            ]
        self.images = [
            [
                "/flash/sys/apps/cccflower/spede_nelio.png",
                -110,
                -110,
                225,
                225
            ],
            [
                "/flash/sys/apps/cccflower/Exploits.png",
                -121,
                -121,
                242,
                242
            ]
        ]

        self.bg_interval = 1400
        self.bg_color = [0.0, 0.0, 0.0]
        self.bg_since_step = 0
        self.bg_steps = [0.0, 0.0, 0.0]
        self.bg_fire_array_index = 0
        
    def draw(self, ctx: Context) -> None:

        ctx.rgb(*self.bg_color).rectangle(-120, -120, 240, 240).fill()

        # Nick is after last image

        if self.image_index == len(self.images):

            ctx.image(*self.burning_flower)

            ctx.text_align = ctx.CENTER
            ctx.text_baseline = ctx.MIDDLE
            ctx.font_size = 60
            ctx.font = ctx.get_font_name(5)

            ctx.rotate(1.755*math.pi)

            ctx.rgb(0.322, 0.322, 0.322)
            ctx.move_to(0, 25)
            ctx.save()

            ctx.text(self.name)
            ctx.restore()
        else:
            ctx.image(
                *self.images[self.image_index]
            )

        for i, led in enumerate(self.led_buffer):
            leds.set_rgb(i, *led)

        leds.update()

    def think(self, ins: InputState, delta_ms: int) -> None:
        self.led_since_step += delta_ms
        self.image_since_step += delta_ms
        self.bg_since_step += delta_ms

        self._phase += delta_ms / 1000
        self._scale = math.sin(self._phase)

        if self.bg_since_step > self.bg_interval:
            self.bg_since_step = 0
            self.bg_fire_array_index = (self.bg_fire_array_index + 1) % len(self.fire_array)
            chosen_color = self.fire_array[self.bg_fire_array_index]
            chosen_color = [c / 255.0 for c in chosen_color]

            self.bg_steps = [
                (chosen_color[i] - self.bg_color[i]) / self.bg_interval
                for i in range(3)
            ]

        self.bg_color = [
            self.bg_color[i] + self.bg_steps[i] * delta_ms
            for i in range(3)
        ]

        rage = 500 * (delta_ms / 1000)

        direction = ins.buttons.app # -1 (left), 1 (right), or 2 (pressed)
        if direction == -1 and self.led_interval < 1000:
            self.led_interval += rage

        elif direction == 1 and self.led_interval > 30:
            self.led_interval -= rage


        if self.led_since_step > self.led_interval:
            self.led_since_step = 0

            indices = list(range(self.led_fire_array_index, len(self.fire_array))) + list(range(0, self.led_fire_array_index))

            for f in indices:
                self.led_buffer[self.i] = self.fire_array[f]
                self.i = (self.i + 1) % 40

            self.led_fire_array_index = (self.led_fire_array_index + 1) % len(self.fire_array)

        if self.image_since_step > self.image_interval:
            self.image_since_step = 0
            self.image_index = (self.image_index + 1) % (len(self.images) + 1)

if __name__ == "__main__":
    st3m.run.run_view(Burn(ApplicationContext()))
