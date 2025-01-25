#!/usr/bin/python3
# -*- coding:utf-8 -*-
from picamera2 import Picamera2
import RPi.GPIO as GPIO

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
from main import print_styled


if os.path.exists(libdir):
    sys.path.append(libdir)


BUTTON_PIN = 26  # Change to your GPIO pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


photos_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')




# Configure logging
logging.basicConfig(level=logging.DEBUG)

def capture_image(camera):
    """Capture an image using Picamera2."""
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        save_path = os.path.join(photos_dir, filename)

        logging.info(f"Capturing image to {save_path}")
        camera.capture_file(save_path)
        logging.info("Image captured successfully")
        return save_path
    except Exception as e:
        logging.error(f"Error capturing image: {e}")
        raise
    


def display_image(image_path):
    """Displays an image on the e-paper display while maintaining aspect ratio."""
    try:
        logging.info("Initializing the e-paper display")
        epd = epd2in66g.EPD()
        epd.init()
        epd.Clear()

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        logging.info(f"Loading image: {image_path}")
        image = Image.open(image_path)
        
        # Calculate the aspect ratio and new dimensions
        display_width = epd.height  # Since we rotate later, we use height
        display_height = epd.width
        
        # Calculate scaling factors for both dimensions
        width_ratio = display_width / image.width
        height_ratio = display_height / image.height
        
        # Use the smaller ratio to maintain aspect ratio
        scale_factor = min(width_ratio, height_ratio)
        
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        
        # Resize image maintaining aspect ratio
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a white background image
        background = Image.new('RGB', (display_width, display_height), 'white')
        
        # Calculate position to center the image
        x = (display_width - new_width) // 2
        y = (display_height - new_height) // 2
        
        # Paste the resized image onto the center of the white background
        background.paste(image, (x, y))
        
        # Rotate for landscape mode
        background = background.rotate(90, expand=True)

        logging.info("Displaying the image on the e-paper")
        epd.display(epd.getbuffer(background))
        time.sleep(3)
    except Exception as e:
        logging.error(f"Error displaying image: {e}")
        sys.exit(1)

 

if __name__ == "__main__":

    try:
        # Initialize camera once before the loop
        picam2 = Picamera2()
        picam2.configure(picam2.create_still_configuration())
        picam2.start()
        logging.info("Camera initialized and warmed up")
        print("Camera initialized and warmed up")

        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                try:
                    # Capture and display image immediately
                    image_path = capture_image(picam2)
                    styled_image = print_styled(image_path)
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    styled_image_name = f"styled_{timestamp}.png"
                    styled_image_path = os.path.join(photos_dir, styled_image_name)
                    styled_image.save(styled_image_path)

                


                    display_image(styled_image_path)

                except Exception as e:
                    logging.error(f"Error in main loop: {e}")
                    # Only close and reinitialize camera if there's an error
                    picam2.close()
                    picam2 = Picamera2()
                    picam2.configure(picam2.create_still_configuration())
                    picam2.start()
                
                time.sleep(1)  # Debounce delay

            time.sleep(0.1)  # Small delay to reduce CPU usage

    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
        if picam2 is not None:
            picam2.close()
        epd2in66g.epdconfig.module_exit(cleanup=True)
        sys.exit(0)
