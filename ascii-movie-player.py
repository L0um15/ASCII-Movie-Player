import sys
import cv2
from fpstimer import FPSTimer
from playsound import playsound

IMAGE_WIDTH = 200
FRAME_FOLDER_PATH = "./frames"
ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']


def resize_image(image, r_width):
    height, width = image.shape
    ratio = height / int(width * 2.5)
    r_height = int(ratio * r_width)
    return cv2.resize(image, (r_width, r_height))

def convert_pixels_to_ascii_table(image):
    height, width = image.shape
    pixels = []
    for i in range(height):
        for j in range(width):
            pixel = image.item(i,j)
            pixels.append(ASCII_CHARS[pixel//25])
    return ''.join(pixels)

def convert_ascii_table_to_image(ascii_table, r_width):
    ascii_character_set = []
    for i in range(0, len(ascii_table), r_width):
        ascii_character_set.append(ascii_table[i:i+r_width])
    return '\n'.join(ascii_character_set)

def move_cursor(x,y):
    print("\033[%d;%dH" % (y,x))

def get_ascii_image(image):
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_grayscaled_image = resize_image(grayscaled_image, IMAGE_WIDTH)
    ascii_table = convert_pixels_to_ascii_table(resized_grayscaled_image)
    ascii_image = convert_ascii_table_to_image(ascii_table, IMAGE_WIDTH)
    return ascii_image

def main():
    video_file_path = sys.argv[1]
    audio_file_path = sys.argv[2]

    video_capture = cv2.VideoCapture(video_file_path)

    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    fps_timer = FPSTimer(frame_rate)

    succ, image = video_capture.read()
    playsound(audio_file_path, block=False)

    while succ:
        print(get_ascii_image(image))
        fps_timer.sleep()
        move_cursor(0,0)
        succ, image = video_capture.read()


if __name__ == '__main__':
    main()
