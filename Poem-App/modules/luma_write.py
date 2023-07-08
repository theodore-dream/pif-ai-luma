#!/bin/env python3

import os, random
import time
from time import sleep
import textwrap
from PIL import ImageFont, ImageDraw

# using luma library for OLED display through SPI 
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351
from luma.core.virtual import viewport

# setup logger
#from modules 
import logger
from logger import setup_logger
logger = setup_logger('luma_log')

serial = spi(device=0, port=0)
device = ssd1351(serial)

# setting up virtual viewport and font for OLED
virtual = viewport(device, width=device.width, height=768)
font = ImageFont.truetype('/home/pi/Documents/pif-ai-luma/Poem-App/fonts/pixelmix.ttf',9)

def text_wrap(text, width):
    """
    Wrap text to fit specified width
    """
    # Split text by new lines
    lines = text.split('\n')

    wrapped_text = []
    for line in lines:
        # Use textwrap to wrap lines that exceed the specified width
        wrapped_line = textwrap.wrap(line, width=24)
        if wrapped_line:
            wrapped_text.extend(wrapped_line)
        else:
            # If the line is empty, maintain it as an empty line
            wrapped_text.append('')

    logger.info(f"text_wrap output: {wrapped_text}")
    return wrapped_text

# Mostly crawl.py example also using http://codelectron.com/setup-oled-display-raspberry-pi-python/ for info

def luma_write(gametext, display_time):
    # first let's make sure device is clear
    device.clear()
    logger.info("Starting luma_write function")

    with canvas(device) as draw:
        lines = []
        # In case gametext is a list of strings
        if isinstance(gametext, list):
            for txt in gametext:
                lines.extend(text_wrap(txt, 18))  # 18 characters per line as you mentioned
        # In case gametext is a single string
        elif isinstance(gametext, str):
            lines.extend(text_wrap(gametext, 18))  # 18 characters per line as you mentioned
        
        # Ensure only the first 10 lines are taken (to fit your 10 lines OLED)
        lines = lines[:20]
        logger.info(f"lines: {lines}")

        # Draw each line on the OLED
        for i, line in enumerate(lines):
            draw.text((0, i * 10), line, font=font, fill="white")
            print("used draw.text")
            #sleep(5)
            #term.println("Hello, World!")
            #print("Use println to print text followed by a newline")
            #sleep(5)
            #term.puts("No newline here.")
            #print("Used puts to print text without a newline")
            #sleep(5)



    # Sleep for the display_time before clearing the screen
    time.sleep(display_time)
    device.clear()
    logger.info("wrote to device")
    device.clear()
    logger.info("device cleared, luma_write function completed")

#lets run it as a unit test
if __name__ == "__main__":
    luma_write("hi hi hi hi hi hi hi no hi hi hi hi hi hi hi no", 15)