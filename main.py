# Header Comment
# Project: [Art Timelapse Maker] [https://github.com/GreenBeanio/Art-Timelapse-Maker]
# Copyright: Copyright (c) [2024]-[2024] [Art Timelapse Maker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to create timelapses from videos.]
# File Description: [Creates the flask and celery apps.]

# Imports
import os
import pathlib
import subprocess
import sys
import argparse
import logging
from typing import List


# Class to store the user arguments
class userArguments:
    def __init__(
        self,
        video_directory,
        audio_directory,
        output_directory,
        temp_directory,
        delete_video,
        delete_audio,
        keep_temp_video,
        keep_temp_audio,
        override_temp_video,
        override_temp_audio,
        override_output,
        clear_temp_video,
        clear_temp_audio,
        clear_output,
        output_fps,
        speed_factor,
    ) -> None:
        self.video_directory = video_directory
        self.audio_directory = audio_directory
        self.output_directory = output_directory
        self.temp_directory = temp_directory
        self.delete_video = delete_video
        self.delete_audio = delete_audio
        self.keep_temp_video = keep_temp_video
        self.keep_temp_audio = keep_temp_audio
        self.override_temp_video = override_temp_video
        self.override_temp_audio = override_temp_audio
        self.override_output = override_output
        self.clear_temp_video = clear_temp_video
        self.clear_temp_audio = clear_temp_audio
        self.clear_output = clear_output
        self.output_fps = output_fps
        self.speed_factor = speed_factor


# Function to make sure passed paths exist
def checkPath(test_path: pathlib.Path) -> bool:
    if pathlib.Path.exists(test_path):
        return True
    else:
        return False


# Function to create directories that don't exist
def createDir(new_path: pathlib) -> None:
    if not pathlib.Path.exists(new_path):
        try:
            pathlib.Path.mkdir(new_path)
        except:
            logger.critical(f"Couldn't create directory at {new_path}")
            sys.exit()


# Function to get the paths to use
def getPaths() -> userArguments:
    # Get the directory where the script was called from
    cwd = pathlib.Path().resolve()
    # Getting the video directory
    if cli_args.video_directory is None:
        video_source_directory = pathlib.Path.joinpath(cwd, "video")
        if not checkPath(video_source_directory):
            logger.critical('No "video" folder in directory or passed video directory')
            sys.exit()
    else:
        if checkPath(cli_args.video_directory):
            video_source_directory = cli_args.video_directory
        else:
            logger.critical("Invalid video source directory")
            sys.exit()
    # Getting the audio directory
    if cli_args.audio_directory is None:
        audio_source_directory = pathlib.Path.joinpath(cwd, "audio")
        if not checkPath(audio_source_directory):
            logger.critical('No "audio" folder in directory or passed audio directory')
            sys.exit()
    else:
        if checkPath(cli_args.audio_directory):
            audio_source_directory = cli_args.audio_directory
        else:
            logger.critical("Invalid audio source directory")
            sys.exit()
    # Getting the output directory
    if cli_args.output_directory is None:
        output_directory = pathlib.Path.joinpath(cwd, "output")
        createDir(output_directory)
    else:
        if checkPath(cli_args.output_directory):
            output_directory = cli_args.output_directory
        else:
            logger.critical("Invalid output directory")
            sys.exit()
    # Getting the temp directory
    if cli_args.temp_directory is None:
        temp_directory = pathlib.Path.joinpath(cwd, "temp")
        createDir(temp_directory)
    else:
        if checkPath(cli_args.temp_directory):
            temp_directory = cli_args.temp_directory
        else:
            logger.critical("Invalid temp directory")
            sys.exit()

    # Getting the bool options
    delete_video = cli_args.delete_source_video
    delete_audio = cli_args.delete_source_audio
    keep_temp_video = cli_args.keep_temp_video
    keep_temp_audio = cli_args.keep_temp_audio
    override_temp_video = cli_args.override_temp_video
    override_temp_audio = cli_args.override_temp_audio
    override_output = cli_args.override_output
    clear_temp_video = cli_args.clear_temp_video
    clear_temp_audio = cli_args.clear_temp_audio
    clear_output = cli_args.clear_output
    output_fps = cli_args.output_fps
    speed_factor = cli_args.speed_factor
    # Return the arguments
    return userArguments(
        video_source_directory,
        audio_source_directory,
        output_directory,
        temp_directory,
        delete_video,
        delete_audio,
        keep_temp_video,
        keep_temp_audio,
        override_temp_video,
        override_temp_audio,
        override_output,
        clear_temp_video,
        clear_temp_audio,
        clear_output,
        output_fps,
        speed_factor,
    )


# Function to get the files from a directory
def getFiles(search_path: pathlib.Path, file_names: List[str]) -> list:
    file_list = []
    for file in search_path.iterdir():
        # check if it's a file
        if not file.is_file():
            continue
        # Check the file type
        if not file.suffix.lower() in file_names:
            continue
        # Add the file
        file_list.append(file)
    return file_list


# Function to create the concat file for ffmpeg
def concatFile(files: List[pathlib.Path], output: pathlib.Path) -> None:
    temp_str = ""
    for file in files:
        temp_str += f"file '{file}'\n"
    with open(output, "w+") as file:
        file.write(temp_str)


# Function to use ffprobe to get the length of the file
def getLength(file: pathlib.Path) -> float:
    terms = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file}"'
    ffprobe = subprocess.Popen(
        terms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # Run the command and get the result
    duration, err = ffprobe.communicate(timeout=30)
    return float(duration)


def getFramerate(file: pathlib.Path) -> float:
    terms = f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "{file}"'
    ffprobe = subprocess.Popen(
        terms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # Run the command and get the result
    result, err = ffprobe.communicate(timeout=30)
    terms = result.split("/")
    framerate = round(float(int(terms[0]) / int(terms[1])), 2)
    return framerate


# Function to create a timelapse from a video
def timelapseVideo(file: pathlib.Path) -> None:
    # print(getLength(file))
    output = pathlib.Path.joinpath(timelapse_args.temp_directory, file.name)
    # Tried to use this method, but I couldn't figure out how to calculate the frames to skip from the multiplier.
    # terms = f'ffmpeg -i "{file}" -vf framestep={every_x_frames},setpts=N/{getFramerate(file)}/TB -c:v libx265 -r {timelapse_args.output_fps} -an "{output}"'
    terms = f'ffmpeg -i "{file}" -vf setpts={1/timelapse_args.speed_factor}*PTS -c:v libx265 -r {timelapse_args.output_fps} -an "{output}"'
    timelapse = subprocess.Popen(
        terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    timelapse.wait()


# Function to combine the timelapse videos
def combineTimelapse(file: pathlib.Path) -> None:
    output = pathlib.Path.joinpath(timelapse_args.output_directory, "timelapse.mp4")
    terms = f'ffmpeg -f concat -safe 0 -i {file} -c copy "{output}"'
    timelapse = subprocess.Popen(
        terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    timelapse.wait()


# Command line arguments
parser = argparse.ArgumentParser(
    prog="Timelapse Maker",
    description="Makes timelapses from video files.",
    epilog="Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio",
)
parser.add_argument(
    "-v", "--video_directory", help="Path to the video directory", type=pathlib.Path
)
parser.add_argument(
    "-a", "--audio_directory", help="Path to the audio directory", type=pathlib.Path
)
parser.add_argument(
    "-o", "--output_directory", help="Path to the output directory", type=pathlib.Path
)
parser.add_argument(
    "-t", "--temp_directory", help="Path to the temp directory", type=pathlib.Path
)
parser.add_argument(
    "-dv",
    "--delete_source_video",
    help="Deletes the source video files if passed",
    action="store_true",
)
parser.add_argument(
    "-da",
    "--delete_source_audio",
    help="Deletes the source audio files if passed",
    action="store_true",
)
parser.add_argument(
    "-ktv",
    "--keep_temp_video",
    help="Doesn't delete the temporary video files if passed",
    action="store_false",
)
parser.add_argument(
    "-kta",
    "--keep_temp_audio",
    help="Doesn't delete the temporary audio files if passed",
    action="store_false",
)
parser.add_argument(
    "-otv",
    "--override_temp_video",
    help="Overrides the temporary video files if passed",
    action="store_true",
)
parser.add_argument(
    "-ota",
    "--override_temp_audio",
    help="Overrides the temporary audio files if passed",
    action="store_true",
)
parser.add_argument(
    "-oo",
    "--override_output",
    help="Overrides the output if passed",
    action="store_true",
)
parser.add_argument(
    "-ctv",
    "--clear_temp_video",
    help="Deletes all the existing temporary video files before creating new files if passed",
    action="store_true",
)
parser.add_argument(
    "-cta",
    "--clear_temp_audio",
    help="Deletes all the existing temporary audio files before creating new files if passed",
    action="store_true",
)
parser.add_argument(
    "-co",
    "--clear_output",
    help="Deletes all the existing output files before creating new files if passed",
    action="store_true",
)
parser.add_argument(
    "-fps",
    "--output_fps",
    help="Defines the output video fps",
    type=float,
    default=30,
)
parser.add_argument(
    "-sf",
    "--speed_factor",
    help="How much do you want to speed up the timelapse by",
    type=float,
    default=30,
)

cli_args = parser.parse_args()
# print(cli_args)

# Create logger
logger = logging.getLogger(__name__)

## Get the command line arguments
timelapse_args = getPaths()

# Get the files
video_files = getFiles(timelapse_args.video_directory, [".mp4", ".mkv"])
audio_files = getFiles(timelapse_args.audio_directory, [".wav", ".mp3"])

# Check if there are videos in the video directory
if len(video_files) == 0:
    logger.critical("There are no videos in the video file")
    sys.exit()

# Turn every video into a timelapse
for video in video_files:
    timelapseVideo(video)
    # Maybe add the ability to crop and transition video clips if wanted

# Create a concat list of all the videos
timelapse_video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
concat_video = pathlib.Path.joinpath(timelapse_args.temp_directory, "video.txt")
concatFile(timelapse_video_files, concat_video)
combineTimelapse(concat_video)
# Remove the video file
##os.remove(concat_video)

# Merge audio files if there are audio files (NOTE: Add transition later)
if len(audio_files) != 0:
    # Path for the audio concat file
    audio_concat = pathlib.Path.joinpath(timelapse_args.temp_directory, "audio.txt")
    # Path for the outputted merged audio
    audio_out = pathlib.Path.joinpath(timelapse_args.output_directory, "audio.wav")
    # Creating the concat file
    concatFile(audio_files, audio_concat)
    # Merge the audio files
    audio_terms = f'ffmpeg -f concat -safe 0 -i "{audio_concat}" -c:a aac "{audio_out}"'
    audio_combine = subprocess.Popen(
        audio_terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    audio_combine.wait()
    # Remove the audio file
    ##os.remove(audio_concat)
    # Add the audio to the video (make sure the combined audio is longer than the video, it will use the shortest)
    video_out = pathlib.Path.joinpath(timelapse_args.output_directory, "timelapse.mp4")
    video_out_audio = pathlib.Path.joinpath(
        timelapse_args.output_directory, "timelapse_audio.mp4"
    )
    audio_terms = f'ffmpeg -i "{video_out}" -i "{audio_out}" -map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
    add_audio = subprocess.Popen(
        audio_terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    add_audio.wait()


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]