import argparse
import os
import subprocess

def run(video_path, frames_path):

    print(f"Extracting frames from {video_path}")

    outer_path = os.path.dirname(video_path)
    stdout_path = os.path.join(outer_path, "output.log")

    ffmpeg_command = ['ffmpeg', '-i', video_path, f"{frames_path}/%05d.png"]
    with open(stdout_path, "a") as f:
        subprocess.run(ffmpeg_command, stdout=f, stderr=subprocess.STDOUT)

def main():
    """
    Takes path to video and extracts frames to given folder
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', type=str, help='Path to input video')
    parser.add_argument('frames_path', type=str, help='Path to output frames')

    args = parser.parse_args()
    video_path = args.video_path.rstrip("/")
    frames_path = args.frames_path.rstrip("/")

    if not os.path.exists(video_path):
        print(f"ERROR: Video doesn't exist")
        exit()

    if not os.path.exists(frames_path):
        os.makedirs(frames_path)

    run(video_path, frames_path)

if __name__ == "__main__":
    main()