import argparse
import os
import shutil


def run(results_folder, cameras_folder):

    for frame_number in os.listdir(results_folder):
        frame_folder = os.path.join(results_folder, frame_number)
        for direction in os.listdir(frame_folder):
            direction_folder = os.path.join(frame_folder, direction, "frames")
            for camera in os.listdir(direction_folder):
                file_name = os.path.join(direction_folder, camera)
                name, ext = os.path.splitext(camera)

                seperated_name = os.path.join(cameras_folder, f"{direction}_{name}")
                print(seperated_name, "--", file_name)
                if not os.path.exists(seperated_name):
                   os.makedirs(seperated_name)

                shutil.copyfile(file_name, f"{seperated_name}/{frame_number}.png")


def main():
    """
    Takes path to ../name/results and seperates cameras that belong together into folders.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('results_folder', type=str, help='Path to ../name/results')
    parser.add_argument('cameras_folder', type=str, help='Path to  ../name/cameras')

    args = parser.parse_args()
    results_folder = args.results_folder.rstrip("/")
    cameras_folder = args.cameras_folder.rstrip("/")

    run(results_folder, cameras_folder)

if __name__ == "__main__":
    main()