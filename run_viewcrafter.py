import argparse
import shutil
import subprocess

import os
import re
import stat
import resource
import json

def run(input_file, output_folder):

    print(f"Running VIEWCRAFTER on {input_file}")
    # in ViewCrafter folder
    ori_script_path = '/home/emmahaidacher/Desktop/viewcrafter/ViewCrafter/run.sh'
    ori_script_folder = os.path.dirname(ori_script_path)
    # todo copy and change script like in mvsplat
    outer_path = input_file.split("/")[0: -2]
    results_path = os.path.join("/", *outer_path, "results.json")
    stdout_path = os.path.join("/", *outer_path, "output.log")

    with open(ori_script_path, 'r') as file:
        script_content = file.read()

    results = {}

    video_length = 12
    temp_script_path = os.path.join(outer_path, "temp_script.sh")

    modified_content = script_content
    modified_content = re.sub(r'--image_dir\s+\S+', f'--image_dir {input_file}', modified_content)
    modified_content = re.sub(r'--out_dir\s+\S+', f'--out_dir {output_folder}', modified_content)
    modified_content = re.sub(r'--video_length\s+\S+', f'--video_length {video_length}', modified_content)
    # modified_content = re.sub(r'python\s+\S+', f'python {modified_script_path}', modified_content)

    for direction in ["left", "right", "up", "down"]:
        modified_content = re.sub(r'--traj_txt\s+\S+', f'--traj_txt test/trajs/{direction}.txt', modified_content)
        with open(temp_script_path, 'w') as file:
            file.write("#!/bin/bash\n")
            file.write("source ~/.zshrc\n")
            file.write(f"cd {ori_script_folder}\n")
            file.write("conda deactivate\n")
            file.write("source /home/emmahaidacher/miniconda3/bin/activate viewcrafter\n")
            # todo get right path to conda env
            file.write(modified_content)
            st = os.stat(modified_script_path)
            os.chmod(modified_script_path, st.st_mode | stat.S_IEXEC)

        original_env = os.environ.copy()
        # https://stackoverflow.com/questions/13889066/run-an-external-command-and-get-the-amount-of-cpu-it-consumed/13933797#13933797
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        with open(stdout_path, "a") as f:
            subprocess.run([modified_script_path], stdout=f, stderr=subprocess.STDOUT)
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_time = usage_end.ru_utime - usage_start.ru_utime
        os.environ.clear()
        os.environ.update(original_env)


    extra_folder = os.path.join(out_dir, os.listdir(out_dir)[0])
    all_files = os.listdir(extra_folder)
    for f in all_files:
        shutil.move(os.path.join(extra_folder, f), out_dir)

    os.rmdir(extra_folder)
    results[name] = {"inference_time": cpu_time, "name": name, "framework": "viewcrafter"}


    print("VIEWCRAFTER Success")


    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
            data["viewcrafter"] = results
    except FileNotFoundError:
        data = {"viewcrafter": results}


    with open(results_path, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    """
    Takes image and runs viewcrafter. This is done by copying the
    original shell file, modifying the --image_dir and --out_dir, adding some terminal commands and then running
    this modified shell scrips.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Path to image to run')
    parser.add_argument('output_path', type=str, help='Path to  ../name/results/0001')

    args = parser.parse_args()
    input_file = args.input_path.rstrip("/")
    output_folder = args.output_path.rstrip("/")

    run(input_file, output_folder)

if __name__ == "__main__":
    main()