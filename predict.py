import os

HOME_DIR = os.environ.get('HOME', '/root')
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

import sys

sys.path.append(BASE_PATH)

from typing import List
import hashlib
import shutil
import subprocess
import tarfile
import zipfile
import json

from cog import BasePredictor, Input, Path
from helpers.comfyui import ComfyUI

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"
COMFYUI_TEMP_OUTPUT_DIR = "ComfyUI/temp"


def build_pip_install_cmds(args):

    if "python_embeded" in sys.executable or "python_embedded" in sys.executable:

        return [sys.executable, '-s', '-m', 'pip', 'install'] + args

    else:

        return [sys.executable, '-m', 'pip', 'install'] + args


def ensure_package(path_file_model=None):
    cmds = build_pip_install_cmds(
        [BASE_PATH + '/extra/transparent-background/'])
    subprocess.run(cmds, cwd=BASE_PATH)


def mkdir_safe(out_path):
    if type(out_path) == str:
        if len(out_path) > 0:
            if not os.path.exists(out_path):
                os.mkdir(out_path)


def hash_file(filename):
    h = hashlib.sha512()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def which(exe_name):

    if exe_name in os.listdir('/usr/local/bin'):
        return '/usr/local/bin/' + exe_name

    if exe_name in os.listdir('/usr/bin'):
        return '/usr/bin/' + exe_name

    if exe_name in os.listdir('/bin'):
        return '/bin/' + exe_name

    return None


def aria2c(url, name):
    subprocess.run(
        [which(exe_name='aria2c'), '-c', '-x16', '-j16', '-o', name, url])


def do_download(url, name, sha512sum, path):
    TMP = HOME_DIR + '/TMP'
    SHA512SUM_DIR = HOME_DIR + '/SHA512SUM'
    mkdir_safe(out_path=SHA512SUM_DIR)

    if not os.path.exists(TMP):
        os.mkdir(TMP)

    if os.path.exists(TMP) and os.path.isdir(TMP):

        file_exists = (sha512sum is not None) and (
            os.path.exists(SHA512SUM_DIR + '/' + sha512sum))

        if not file_exists:

            os.chdir(TMP)
            os.system('pwd ; ls')
            if ((not os.path.exists(name)) and
                (not os.path.exists(name + '.aria2'))) or (
                    (os.path.exists(name)) and
                    (os.path.exists(name + '.aria2'))):

                aria2c(url=url, name=name)

        os.chdir(TMP)
        os.system('pwd ; ls')
        if os.path.exists(name) and (not os.path.exists(name + '.aria2')):

            hash = hash_file(filename=name)

            if sha512sum is not None:
                if sha512sum == hash:
                    shutil.move(name, SHA512SUM_DIR + '/' + hash)

        file_exists = (sha512sum is not None) and (
            os.path.exists(SHA512SUM_DIR + '/' + sha512sum))

        if path is not None:

            if file_exists:
                if os.path.exists(path):
                    os.unlink(path)

                os.symlink(src=SHA512SUM_DIR + '/' + sha512sum, dst=path)

    else:
        print('Failed to make the TMP directory.')


def get_workflow(input_file_background, input_file_subject):
    with open(BASE_PATH + '/workflow_api.json', "r") as file:
        WORKFLOW = file.read()
    WORKFLOW = json.loads(WORKFLOW)
    WORKFLOW["3"]["inputs"]["image"] = input_file_background
    WORKFLOW["4"]["inputs"]["image"] = input_file_subject
    return WORKFLOW


def download_inspyrenet():
    DEST_DIR = BASE_PATH + '/models/inspyrenet/'
    mkdir_safe(out_path=DEST_DIR)

    do_download(
        url=
        'https://huggingface.co/hanamizuki-ai/InSPyReNet-SwinB-Plus-Ultra/resolve/main/latest.pth',
        name='InSPyReNet-SwinB-Plus-Ultra.pth',
        sha512sum=
        '542ad8974e0c8f8ec041f446176e7380642fc5c331b3239c8197775780b1ac8dc7311bf2edebb8c1d12741eda1f510bc4c4f24ed8c1ae92dcf00612360b03dee',
        path=DEST_DIR + '/InSPyReNet-SwinB-Plus-Ultra.pth',
    )


class Predictor(BasePredictor):

    def setup(self):
        download_inspyrenet()
        ensure_package(path_file_model=None)
        os.chdir(BASE_PATH)
        self.comfyUI = ComfyUI("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR, INPUT_DIR)

    def cleanup(self):
        self.comfyUI.clear_queue()
        for directory in [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)

    def handle_input_file(self, input_file: Path):
        file_extension = os.path.splitext(input_file)[1].lower()
        if file_extension == ".tar":
            with tarfile.open(input_file, "r") as tar:
                tar.extractall(INPUT_DIR)
        elif file_extension == ".zip":
            with zipfile.ZipFile(input_file, "r") as zip_ref:
                zip_ref.extractall(INPUT_DIR)
        elif file_extension in [".jpg", ".jpeg", ".png", ".webp"]:
            shutil.copy(input_file,
                        os.path.join(INPUT_DIR, f"input{file_extension}"))
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        print("====================================")
        print(f"Inputs uploaded to {INPUT_DIR}:")
        self.log_and_collect_files(INPUT_DIR)
        print("====================================")

    def log_and_collect_files(self, directory, prefix=""):
        files = []
        for f in os.listdir(directory):
            if f == "__MACOSX":
                continue
            path = os.path.join(directory, f)
            if os.path.isfile(path):
                print(f"{prefix}{f}")
                files.append(Path(path))
            elif os.path.isdir(path):
                print(f"{prefix}{f}/")
                files.extend(
                    self.log_and_collect_files(path, prefix=f"{prefix}{f}/"))
        return files

    def predict(
        self,
        input_file_background: Path = Input(
            description="Input image of background",
            default=None,
        ),
        input_file_subject: Path = Input(
            description="Input image of subject",
            default=None,
        ),
        randomise_seeds: bool = Input(
            description=
            "Automatically randomise seeds (seed, noise_seed, rand_seed)",
            default=True,
        ),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        self.cleanup()

        self.handle_input_file(input_file_background)
        self.handle_input_file(input_file_subject)

        # TODO: Record the previous models loaded
        # If different, run /free to free up models and memory

        wf = self.comfyUI.load_workflow(
            get_workflow(input_file_background, input_file_subject))

        if randomise_seeds:
            self.comfyUI.randomise_seeds(wf)

        self.comfyUI.connect()
        self.comfyUI.run_workflow(wf)

        files = []
        output_directories = [OUTPUT_DIR]
        if return_temp_files:
            output_directories.append(COMFYUI_TEMP_OUTPUT_DIR)

        for directory in output_directories:
            print(f"Contents of {directory}:")
            files.extend(self.log_and_collect_files(directory))

        return files
