import sys
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

ASCII_CHARS = "@%#*+=-:. "
FONT_SIZE = 10  # Adjust as needed

def enhance_color(color, factor=2.5):  # Increase factor to enhance vibrance
    return tuple(min(int(comp * factor), 255) for comp in color)

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def pixels_to_ascii_and_color(image):
    pixels = image.getdata()
    ascii_and_color = []
    for pixel in pixels:
        if isinstance(pixel, tuple):
            average = sum(pixel[:3]) // 3
        else:
            average = pixel
            pixel = (average, average, average)  # Convert grayscale to RGB
        index = average * len(ASCII_CHARS) // 256
        ascii_char = ASCII_CHARS[index]
        ascii_and_color.append((ascii_char, enhance_color(pixel)))
    return ascii_and_color

def load_image(path_or_url):
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        response = requests.get(path_or_url)
        image = Image.open(BytesIO(response.content))
    else:
        image = Image.open(path_or_url)
    return image

def main(new_width=100):
    try:
        path_or_url = input("Enter a valid pathname to an image or an image URL:\n")
        image = load_image(path_or_url)
    except Exception as e:
        print(e)
        return

    image = resize_image(image)

    ascii_and_color = pixels_to_ascii_and_color(image)
    img_width = image.width

    # Create a new image for the colored ASCII art
    font = ImageFont.load_default()
    new_img_width = img_width * FONT_SIZE
    new_img_height = len(ascii_and_color) // img_width * FONT_SIZE
    ascii_img = Image.new('RGB', (new_img_width, new_img_height), color="black")
    d = ImageDraw.Draw(ascii_img)

    # Draw each ASCII character with the original color
    x, y = 0, 0
    for i in range(len(ascii_and_color)):
        if i % img_width == 0 and i != 0:
            x = 0
            y += FONT_SIZE
        ascii_char, color = ascii_and_color[i]
        d.text((x, y), ascii_char, font=font, fill=color)
        x += FONT_SIZE

    ascii_img.save('colorful_ascii_art.png')

main()
