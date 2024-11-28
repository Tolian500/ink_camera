from PIL import Image, ImageOps, ImageFilter
import numpy as np
import time

# Input image path
input_image = "example.jpg"

# Generate unique filenames using timestamps
timestamp = int(time.time())
output_smoothed = f"smoothed_{timestamp}.png"
output_edges = f"edges_{timestamp}.png"
output_colored = f"color_book_{timestamp}.png"

# Step 1: Resize to 800x480 without stretching
def resize_image_with_crop(image, target_width, target_height):
    image_aspect_ratio = image.width / image.height
    target_aspect_ratio = target_width / target_height

    if image_aspect_ratio > target_aspect_ratio:
        # Wider than target
        new_height = target_height
        new_width = int(target_height * image_aspect_ratio)
    else:
        # Taller than target
        new_width = target_width
        new_height = int(target_width / image_aspect_ratio)

    image = image.resize((new_width, new_height), Image.LANCZOS)

    # Center crop to target size
    left = (image.width - target_width) / 2
    top = (image.height - target_height) / 2
    right = left + target_width
    bottom = top + target_height

    return image.crop((left, top, right, bottom))

# Step 2: Reduce noise with smoothing
def smooth_image(image):
    return image.filter(ImageFilter.MedianFilter(size=3))

# Step 3: Detect edges to create bold outlines
def detect_edges(image):
    # Convert to grayscale for edge detection
    grayscale = ImageOps.grayscale(image)
    # Use edge detection filter
    edges = grayscale.filter(ImageFilter.FIND_EDGES)
    # Invert colors for bold black lines on white
    inverted_edges = ImageOps.invert(edges)
    return inverted_edges

# Step 4: Reduce colors to red, yellow, black, and white
def color_quantization(image):
    # Define custom palette
    palette = [
        (255, 0, 0),    # Red
        (255, 255, 0),  # Yellow
        (0, 0, 0),      # Black
        (255, 255, 255) # White
    ]
    
    # Convert to grayscale for simpler processing
    grayscale = ImageOps.grayscale(image)
    np_image = np.array(grayscale)

    # Map pixel values to nearest color in the palette
    thresholds = [64, 128, 192]  # Divide grayscale into 4 ranges
    quantized = np.zeros_like(np_image)
    for i, threshold in enumerate(thresholds):
        quantized[np_image >= threshold] = (i + 1) * 64

    # Map quantized values to colors
    colored_array = np.zeros((np_image.shape[0], np_image.shape[1], 3), dtype=np.uint8)
    for i, color in enumerate(palette):
        mask = quantized == (i * 64)
        colored_array[mask] = color

    return Image.fromarray(colored_array, mode="RGB")

# Main process
if __name__ == "__main__":
    # Load image
    img = Image.open(input_image)

    # Step 1: Resize without stretching
    img_resized = resize_image_with_crop(img, 800, 480)

    # Step 2: Smooth the image to reduce noise
    img_smoothed = smooth_image(img_resized)
    img_smoothed.save(output_smoothed)

    # Step 3: Detect edges for outlines
    img_edges = detect_edges(img_smoothed)
    img_edges.save(output_edges)

    # Step 4: Apply color quantization
    img_colored = color_quantization(img_smoothed)
    img_colored.save(output_colored)

    print("Processing complete. Images saved as:")
    print(f"Smoothed image: {output_smoothed}")
    print(f"Edges image: {output_edges}")
    print(f"Coloring book image: {output_colored}")
