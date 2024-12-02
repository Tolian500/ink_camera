#!/usr/bin/python3
# -*- coding:utf-8 -*-
from picamera2 import Picamera2


import sys
import os
import logging

# Ensure the lib directory is included in the Python path
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in66g



from PIL import Image
import traceback
import time
from printImage import display_image as display_image_styled


if os.path.exists(libdir):
    sys.path.append(libdir)

photos_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')




# Configure logging
logging.basicConfig(level=logging.DEBUG)

def capture_image(camera):
    """Capture an image using Picamera2."""
    try:
        logging.info("Initializing the Picamera2")

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        save_path = os.path.join(photos_dir, filename)


        picam2 = camera
        picam2.start()
        time.sleep(2)  # Allow the camera to adjust
        logging.info(f"Capturing image to {save_path}")
        picam2.capture_file(save_path)
        logging.info("Image captured successfully")
        picam2.stop()
        return save_path
    except Exception as e:
        logging.error(f"Error capturing image: {e}")
        sys.exit(1)
    


def display_image(image_path):
    """Displays an image on the e-paper display."""
    try:
        logging.info("Initializing the e-paper display")
        epd = epd2in66g.EPD()
        epd.init()
        epd.Clear()

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        logging.info(f"Loading image: {image_path}")
        image = Image.open(image_path)
        image = image.resize((epd.height, epd.width))  # Resize to fit display
        image = image.rotate(270, expand=True)  # Rotate for landscape mode

        logging.info("Displaying the image on the e-paper")
        epd.display(epd.getbuffer(image))
        time.sleep(3)
    except Exception as e:
        logging.error(f"Error displaying image: {e}")
        sys.exit(1)

 

if __name__ == "__main__":
    try:
        # Initialize camera
        picam2 = Picamera2()
        picam2.configure(picam2.create_still_configuration())

        # Capture the image
        image_path = capture_image(picam2)

        # Display the image
        display_image(image_path)

    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
        epd2in66g.epdconfig.module_exit(cleanup=True)
        sys.exit(0)
