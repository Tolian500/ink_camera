from PIL import Image, ImageOps

# Step 1: Read the image
input_image_path = "example.jpg"
output_grayscale = "grayshade.png"
output_colored = "colored.png"

# Step 2: Resize to 800x480 without stretching
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

# Step 3: Convert to grayscale
def convert_to_grayscale(image):
    return ImageOps.grayscale(image)

# Step 4: Reduce shades to 4 colors using dithering
def reduce_to_4_shades(image):
    return image.convert("P", palette=Image.ADAPTIVE, colors=4)

# Step 5: Apply red, yellow, black, and white colors
def apply_custom_palette(image):
    palette = [
        255, 255, 255,  # White
        255, 0, 0,      # Red
        255, 255, 0,    # Yellow
        0, 0, 0         # Black
    ]
    
    # Map the 4 reduced colors to the custom palette
    colored_image = Image.new("P", image.size)
    colored_image.putpalette(palette * 64)  # Extend the palette to fit 256 colors
    colored_image.paste(image)
    return colored_image.convert("RGB")


def print_styled(custom_image_path):

    # Load the image
    img = Image.open(custom_image_path)
    # Step 2: Resize without stretching
    img_resized = resize_image_with_crop(img, 800, 480)
    
    # Step 3: Convert to grayscale
    img_grayscale = convert_to_grayscale(img_resized)
    img_grayscale.save(output_grayscale)
    
    # Step 4: Reduce to 4 shades
    img_4_shades = reduce_to_4_shades(img_grayscale)
    
    # Step 5: Apply custom colors
    img_colored = apply_custom_palette(img_4_shades)
    return img_colored



    
# Main process
if __name__ == "__main__":

    print_styled(input_image_path)

    print("Processing complete. Images saved:")
    print(f"Grayscale image: {output_grayscale}")
    print(f"Colored image: {output_colored}")
