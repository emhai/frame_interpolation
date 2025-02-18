import argparse

import cv2
import os

def run(input_folder):

    name = os.path.basename(input_folder)
    outer_folder = os.path.dirname(input_folder)
    video_name = f"{name}.avi"
    video_path = os.path.join(outer_folder, video_name)

    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_path, 0, 15, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(input_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def main():
    """
    takes folder and created video in one folder out
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str, help='Path to image to run')

    args = parser.parse_args()
    input_folder = args.input_folder.rstrip("/")

    run(input_folder)

if __name__ == "__main__":
    main()