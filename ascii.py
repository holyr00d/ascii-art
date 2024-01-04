import sys
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ''
    for pixel in pixels:
        index = pixel * len(ASCII_CHARS) // 256
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def main(new_width=100):
    try:
        path = input("Enter a valid pathname to an image:\n")
        image = Image.open(path)
    except Exception as e:
        print(e)
        return
    
    image = resize_image(image)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""

    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"

    with open("ascii_image.txt", "w") as f:
        f.write(ascii_img)

main()
