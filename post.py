from PIL import Image, ImageOps
import numpy as np

# Input and output paths
input_image = "example.jpg"
output_colored = "custom_colored.png"

# Step 1: Resize to 800x480 without stretching
def resize_image_with_crop(image, target_width, target_height):
    # Calculate the aspect ratio of the image and the target dimensions
    image_aspect_ratio = image.width / image.height
    target_aspect_ratio = target_width / target_height
    
    # Determine the dimensions for cropping
    if image_aspect_ratio > target_aspect_ratio:
        # Wider than target
        new_height = target_height
        new_width = int(target_height * image_aspect_ratio)
    else:
        # Taller than target
        new_width = target_width
        new_height = int(target_width / image_aspect_ratio)
    
    # Resize with the new dimensions
    image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Center crop to target size
    left = (image.width - target_width) / 2
    top = (image.height - target_height) / 2
    right = left + target_width
    bottom = top + target_height
    
    return image.crop((left, top, right, bottom))

# Step 2: Convert to grayscale with 12 tones
def convert_to_12_grayscale(image):
    # Convert image to grayscale
    grayscale = ImageOps.grayscale(image)
    # Map pixel values to 12 tones
    np_image = np.array(grayscale)
    tone_step = 256 // 12
    quantized = (np_image // tone_step) * tone_step
    return Image.fromarray(quantized, mode="L")

# Step 3: Map tones to repeating colors
def map_tones_to_colors(image):
    # Define repeating color palette (red, yellow, black, white)
    palette = [
        (255, 0, 0),    # Red
        (255, 255, 0),  # Yellow
        (0, 0, 0),      # Black
        (255, 255, 255) # White
    ]
    
    # Get pixel data from grayscale image
    np_image = np.array(image)
    
    # Map each tone to a color
    tone_step = 256 // 12
    colored_array = np.zeros((np_image.shape[0], np_image.shape[1], 3), dtype=np.uint8)
    for i in range(12):
        mask = (np_image >= i * tone_step) & (np_image < (i + 1) * tone_step)
        color = palette[i % len(palette)]
        colored_array[mask] = color
    
    # Create a new RGB image from the colored array
    return Image.fromarray(colored_array, mode="RGB")

# Main process
if __name__ == "__main__":
    # Load the image
    img = Image.open(input_image)
    
    # Step 1: Resize without stretching
    img_resized = resize_image_with_crop(img, 800, 480)
    
    # Step 2: Convert to 12 grayscale tones
    img_12_tones = convert_to_12_grayscale(img_resized)
    
    # Step 3: Map tones to repeating colors
    img_colored = map_tones_to_colors(img_12_tones)
    img_colored.save(output_colored)

    print("Processing complete. Colored image saved as:", output_colored)
