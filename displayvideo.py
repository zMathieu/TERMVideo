#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import tempfile
import time
from math import sqrt

import cv2
import numpy as np
import youtube_dl

from palette import palette

palette = np.asarray(palette)
green_colors = [2, 10, 22, 28, 29, 34, 35, 36, 40, 41, 42, 43, 46, 47, 48, 49, 50, 58, 64, 65, 70, 71, 72, 76, 77, 78, 79, 82, 83, 84, 85, 100, 106, 107, 108, 112, 113, 114, 115, 118, 119, 120, 121, 142, 143, 148, 149, 150, 154, 155, 156, 157]
# green_colors = [2, 10, 22, 28, 29, 34, 35, 36, 40, 41, 42, 46, 47, 48, 49, 58, 64, 65, 70, 71, 72, 76, 77, 82, 83, 84, 101, 106, 107, 112, 113, 114, 118, 119, 120, 142, 143, 148, 149, 150, 154, 155, 156]
# green_colors = [2, 10, 22, 28, 29, 34, 35, 40, 41, 42, 46, 47, 48, 64, 70, 71, 76, 77, 82, 83, 106, 112, 113, 118, 119, 148, 149, 154, 155]
# green_colors = [2, 10, 22, 28, 34, 35, 40, 41, 46, 47, 70, 76, 77, 82, 83, 112, 113, 118, 154]


def closest_color(color):
    deltas = palette - color
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)


def display_image(image, width, height, green_bg=False):
    # Make output buffer
    buffer = ''
    for y in range(len(image)):
        for x in range(len(image[0])):
            pixel = image[y][x]
            pixel = pixel[2], pixel[1], pixel[0]
            index = closest_color(pixel)
            if green_bg and index in green_colors:
                buffer += f' '
            else:
                buffer += f'\033[48;5;{index}m \033[0m'
        buffer += '\n'
    # Display image
    print(buffer[:-1], end='')


def display_video(video_path, frame_rate=300, green_bg=False):
    # Get screen size
    columns, rows = os.get_terminal_size(0)
    # Display video
    prev = 0
    capture = cv2.VideoCapture(video_path)
    while True:
        time_elapsed = time.time() - prev
        ret, frame = capture.read()
        if ret:
            if time_elapsed > 1./frame_rate:
                resized = cv2.resize(frame, (columns, rows))
                display_image(resized, columns, rows, green_bg)
                prev = time.time()
        else:
            break

def download_youtube_video(url, max_video_height=360):
    tmp_video_filename = tempfile.mktemp(dir='/tmp')

    ydl_opts = {
        'format': f'bestvideo[height<={max_video_height}]',
        'outtmpl': tmp_video_filename
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return tmp_video_filename


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s <youtube_url>' % sys.argv[0])
        sys.exit(1)

    video_file = download_youtube_video(sys.argv[1])
    display_video(video_file, green_bg=False)
    os.remove(video_file)
