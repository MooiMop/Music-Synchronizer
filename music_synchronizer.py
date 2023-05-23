"""This short script offers a solution to a very niche problem:
you want to have two mirrored directories, where one (PATH_LOSSLESS)
contains music in high quality flacs, and the other (PATH_IPOD) condains
the same files but converted to an iPod-friendly format.
"""

__author__ = "MooiMop"
__version__ = "1.0"

# Import libraries
import subprocess
import os
import pydub
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import mediainfo

# Set global paths
PATH_LOSSLESS = "./Test Music"
PATH_IPOD = "./Test Output"


def batch_process(list_copy, list_convert):
    pbar = tqdm(list_copy, desc="Copying files...")
    for file in pbar:
        output_file = file.replace(PATH_LOSSLESS, PATH_IPOD)
        check_directory(output_file)
        filename = os.path.basename(file)
        pbar.set_description(filename)
        subprocess.run(["cp", file, output_file])
    tricky_files = []
    pbar = tqdm(list_convert, desc="Converting files...")
    for file in pbar:
        filename = os.path.basename(file)
        pbar.set_description(filename)
        if not convert_to_aac(file):
            tricky_files.append(file)
    print(tricky_files)


def check_directory(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def compare_dirs(main, secondary):
    list_copy = []
    list_convert = []
    for dirpath, dirnames, filenames in os.walk(main):
        for filename in filenames:
            file_extension = filename.split(".")[-1]
            new = os.path.join(dirpath, filename).replace(main, secondary)

            if not os.path.exists(new):
                if file_extension in ["mp3", "m4a", "alac"]:
                    list_copy.append(os.path.join(dirpath, filename))
                elif file_extension in ["flac", "FLAC"]:
                    if not os.path.exists(new.replace(file_extension, "m4a")):
                        list_convert.append(os.path.join(dirpath, filename))
    print("Files to copy: " + str(len(list_copy)))
    print("Files to convert: " + str(len(list_convert)))
    return (list_copy, list_convert)


def convert_to_aac(input_file):
    file_extension = input_file.split(".")[-1]

    # Set file destination
    output_file = input_file.replace(file_extension, "m4a").replace(
        PATH_LOSSLESS, PATH_IPOD
    )
    check_directory(output_file)

    # Get the metadata tags from the input file.
    metadata = mediainfo(input_file).get("TAG", {})
    if "comment" in metadata:
        del metadata["comment"]

    metadata_options = []
    for key, value in metadata.items():
        metadata_options.extend(["-metadata", f"{key}={value}"])

    try:
        # Export the AudioSegment object as a WAV file.
        audio = AudioSegment.from_file(input_file, format=file_extension)
        audio.export("temp.wav", format="wav", tags=metadata)

        # Convert the temp file to m3a
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-i", "temp.wav",
                "-codec:a", "aac",
                "-b:a", "320k",
                "-ar", "44100",
                "-ac","2",
                "-y",
                *metadata_options,
                output_file,
            ]
        )
        return True

    except pydub.exceptions.CouldntEncodeError:
        return False

    except pydub.exceptions.CouldntDecodeError:
        return False


copy, convert = compare_dirs(PATH_LOSSLESS, PATH_IPOD)
batch_process(copy, convert)
