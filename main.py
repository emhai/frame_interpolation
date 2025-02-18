import argparse
import os
import resource
import shutil
from datetime import datetime

from PIL import Image
from pandas import wide_to_long

import run_viewcrafter
import extract_frames
import seperate_cameras
import create_video

def create_folder_structure(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print('Created folder:', folder)


def run(path, name):

    main_folder_path = os.path.join("/media/emmahaidacher/Volume/RESULTS", name)
    time = datetime.now().strftime("%m%d_%H%M")

    if name is None:
        folder_name = os.path.basename(path)
        name = f"{folder_name}_{time}"

    if os.path.exists(main_folder_path):
        name = f"{name}_{time}"
        main_folder_path = os.path.join("/media/emmahaidacher/Volume/RESULTS", name)

    os.makedirs(main_folder_path)

    frames_path = os.path.join(main_folder_path, "frames")
    results_path = os.path.join(main_folder_path, "results")
    cameras_path = os.path.join(main_folder_path, "cameras")

    all_folders = [frames_path, results_path, cameras_path]
    create_folder_structure(all_folders)

    # copy video
    video_name, video_ext = os.path.splitext(path)
    video_path = os.path.join(main_folder_path, f"video{video_ext.lower()}")
    shutil.copyfile(path, video_path)
    print(f"Copying video from {path} to {video_path}")

    # extract frames
    extract_frames.run(video_path, frames_path)
    # rename
    filenames = sorted([f for f in os.listdir(frames_path)])
    for file in filenames:
        name, ext = os.path.splitext(file)
        input_file = os.path.join(frames_path, file)
        output_folder = os.path.join(results_path, name)
        run_viewcrafter.run(input_file, output_folder)

    seperate_cameras.run(results_path, cameras_path)

    camera_files = [f for f in os.listdir(cameras_path)]
    for file in camera_files:
        create_video.run(os.path.join(cameras_path, file))

def main():
    """
    Pipeline:   1. todo choose pictures
                2. create folder ../name
                3. copy images to ../name/original_images
                   run colmap to get tranfsorms.json
                   run visualize cameras
                4. create pairwise combinations of variable length to ../name/input
                5. process each combination with viewcrafter to ../name/output
                6. create cropped ground truth images to ../name/cropped_images
                7. todo choose ground truth images
                8. evaluate metrics
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str, help='Path to the video')
    parser.add_argument('name', type=str, nargs='?', default=None, help='Name of test (optional)')

    args = parser.parse_args()
    path = args.path.rstrip("/") # video
    name = args.name # name of test

    usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
    run(path, name)
    usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu_time = usage_end.ru_utime - usage_start.ru_utime
    print(f"CPU time of {cpu_time} seconds")
    print(f"CPU time of {cpu_time / 60} minutes")
    print(f"CPU time of {cpu_time / 60 / 60} hours")


if __name__ == "__main__":
    main()