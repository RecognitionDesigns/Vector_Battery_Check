#!/usr/bin/env python3

import anki_vector
import time
from math import ceil
from anki_vector.util import degrees
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from PIL import Image, ImageDraw, ImageFont

def make_text_image(text_to_draw, x, y, font=None):
    dimensions = (184, 96)
    text_image = Image.new('RGBA', dimensions, (0, 0, 0, 255))
    dc = ImageDraw.Draw(text_image)
    dc.text((x, y), text_to_draw, fill=(0, 255, 0, 255), font=font)
    return text_image

try:
    font_file = ImageFont.truetype("lcd.ttf", 70)
except IOError:
    try:
        font_file = ImageFont.truetype("arial.ttf", 27)
    except IOError:
        pass

with anki_vector.Robot() as robot:
    battery_state = robot.get_battery_state()
    print("Vectors battery is currently {:0.2f} volts".format(battery_state.battery_volts))
    robot.behavior.set_head_angle(degrees(30.0))
    robot.behavior.set_lift_height(0.0)

    face_sum = (str("{:0.2f}".format(battery_state.battery_volts)) + " V")
    text_to_draw = face_sum
    face_image = make_text_image(text_to_draw, 2, 20, font_file)
    args = anki_vector.util.parse_command_args()

    print("Display image on Vector's face...")
    screen_data = anki_vector.screen.convert_image_to_screen_data(face_image)
    robot.screen.set_screen_with_image_data(screen_data, 10.0, interrupt_running=True)
    robot.behavior.say_text("Battery Voltage currently at {:0.2f} volts".format(battery_state.battery_volts))
    time.sleep(2)
