#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from waveshare_epd import epd2in66g
from PIL import Image
import traceback
import time

# Setup paths
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def display_image(image_path):
    """Displays an image on the e-paper display."""
    try:
        logging.info("Initializing the e-paper display")
        epd = epd2in66g.EPD()
        epd.init()
        epd.Clear()

        # Load the image
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        logging.info(f"Loading image: {image_path}")
        image = Image.open(image_path)

        # Ensure image dimensions match display (horizontal orientation)
        image = image.resize((epd.height, epd.width))  # Resize to fit display
        image = image.rotate(270, expand=True)  # Rotate for landscape mode

        # Display the image
        logging.info("Displaying the image on the e-paper")
        epd.display(epd.getbuffer(image))
        time.sleep(3)

    except IOError as e:
        logging.error(f"I/O Error: {e}")
    except FileNotFoundError as e:
        logging.error(f"File Error: {e}")
    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
        epd2in66g.epdconfig.module_exit(cleanup=True)
        exit()
    except Exception as e:
        logging.error(f"Unexpected error: {traceback.format_exc()}")


if __name__ == '__main__':
    # Example usage
    example_image = "example.jpg"  # Replace with the path to your processed image
    display_image(example_image)
