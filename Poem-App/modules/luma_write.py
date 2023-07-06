#!/bin/env python3

import os, random
import time
from time import sleep
import textwrap

# using luma library for OLED display through SPI 
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from luma.core.virtual import viewport

# setup logger
from modules import logger
from modules.logger import setup_logger

logger = setup_logger('luma_log')

serial = spi(device=0, port=0)
device = ssd1351(serial)

from PIL import ImageFont, ImageDraw

def text_wrap(text, width):
    """
    Wrap text to fit specified width
    """
    # Split text by new lines
    lines = text.split('\n')

    wrapped_text = []
    for line in lines:
        # Use textwrap to wrap lines that exceed the specified width
        wrapped_line = textwrap.wrap(line, width=width)
        if wrapped_line:
            wrapped_text.extend(wrapped_line)
        else:
            # If the line is empty, maintain it as an empty line
            wrapped_text.append('')

    return wrapped_text

# Mostly crawl.py example also using http://codelectron.com/setup-oled-display-raspberry-pi-python/ for info

def luma_write(gametext, display_time):
    # first let's make sure device is clear
    device.clear()
    logger.info("Starting luma_write function")

    virtual = viewport(device, width=device.width, height=768)
    font = ImageFont.truetype('/home/pi/Documents/pif-ai-luma/Poem-App/fonts/pixelmix.ttf',9)

    for _ in range(1):
        with canvas(device) as draw:

            # setup variable in scope of function
            lines = []  # Declare 'lines' before the conditions

            # new conditional statement to check if it is a string or a list
            if isinstance(gametext, list):
                lines = text_wrap(gametext, 18)  # Wrap the text to 18 characters
                lines = lines[:10] # Keep only the first 11 lines
            elif isinstance(gametext, str):
                lines = gametext
            for i, line in enumerate(lines):
                draw.text((0, 0 + (i * 12)), text=line, font=font, fill="white")

    logger.info("wrote to device")
    time.sleep(display_time)
    logger.info("clearing device")
    device.clear()
    logger.info("device cleared, luma_write function completed successfully")

