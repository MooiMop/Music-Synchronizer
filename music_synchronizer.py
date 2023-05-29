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
from tqdm import tqdm
import ffmpeg
from joblib import Parallel, delayed

# Set global paths
PATH_LOSSLESS = "./Music"
PATH_IPOD = "./iPod"
WORKERS = 4


def batch_process(list_copy, list_convert):
    pbar = tqdm(list_copy, desc="Copying files...")
    for file in pbar:
        output_file = file.replace(PATH_LOSSLESS, PATH_IPOD)
        check_directory(output_file)
        subprocess.run(["cp", file, output_file])
    
    pbar = tqdm(list_convert, desc="Converting files...")
    # Parallel execution using joblib and tqdm
    with Parallel(n_jobs=WORKERS) as parallel:
        # Wrap the parallel execution with tqdm to track progress
        tricky_files = parallel(delayed(convert_to_mp3)(file) for file in pbar)
    
    tricky_files = [x for x in tricky_files if x is not None]
    if len(tricky_files) > 0:
        print('These files caused errors: ')
        print(tricky_files)
    print('All done!')
    

    #for file in pbar:
    #    filename = os.path.basename(file)
    #    pbar.set_description(filename)
    #    if not convert_to_mp3(file):
    #        tricky_files.append(file)
    #print(tricky_files)


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
                if file_extension in ["mp3"]:
                    list_copy.append(os.path.join(dirpath, filename))
                elif file_extension in ["flac", "FLAC", "m4a"]:
                    if not os.path.exists(new.replace(file_extension, "mp3")):
                        list_convert.append(os.path.join(dirpath, filename))

    print("Files to copy: " + str(len(list_copy)))
    print("Files to convert: " + str(len(list_convert)))
    return (list_copy, list_convert)


def convert_to_mp3(input_file):
    # Set file destination
    file_extension = input_file.split(".")[-1]
    output_file = input_file.replace(file_extension, "mp3").replace(
        PATH_LOSSLESS, PATH_IPOD
    )
    check_directory(output_file)

    # Convert to m4a
    try:
        (
            ffmpeg
            .input(input_file)
            .output(
                output_file,
                **{
                    'c:a': 'libmp3lame',
                    'aq': '2',
                    'hide_banner': None,
                    'loglevel': 'error',
                }
            )
            .overwrite_output()
            .run()
        )
        return None
    except:
        return input_file


copy, convert = compare_dirs(PATH_LOSSLESS, PATH_IPOD)
batch_process(copy, convert)