# Mirroring Music directories for iPod

This script solves a very niche problem wherein you want to keep two mirrored directories that contain the same music tracks in different formats. One directory contains high-quality flac tracks, while the other directory contains the same tracks converted to an iPod-friendly format.

**Author**: MooiMop

**Version**: 1.0

## Requirements
- pydub
- tqdm

## Usage
1. Install requirements using pip:

``` 
pip install -r tqdm ffmpeg-python
```

2. Change the PATH_LOSSLESS and PATH_IPOD variables. They represent the input path and output path of directories respectively.
```
    PATH_LOSSLESS = "./Music"
    PATH_IPOD = "./iPod"
```
3. Run the script:
```
python music_synchronizer.py
```

The script will copy all the mp3 or m4a files to iPod directory, while converting all the FLAC files to m4a format. After running, you will have two mirrored directories with identical content, one in high quality FLACs while the other suitable for iPods.