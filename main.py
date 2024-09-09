# Header Comment
# Project: [Art Timelapse Maker] [https://github.com/GreenBeanio/Art-Timelapse-Maker]
# Copyright: Copyright (c) [2024]-[2024] [Art Timelapse Maker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to create timelapses from videos.]
# File Description: [Creates timelapses from videos (specifically for art).]

# Imports
import os
import pathlib
import subprocess
import sys
import argparse
import logging
from typing import List
import time


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
        verbose,
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
        self.verbose = verbose


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
    verbose = cli_args.verbose
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
        verbose,
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
def concatFile(files: List[pathlib.Path], output: pathlib.Path, utype: str) -> None:
    logger.info(f'Creating the {utype} concat file at "{output}"')
    temp_str = ""
    for file in files:
        temp_str += f"file '{file}'\n"
    with open(output, "w+") as file:
        file.write(temp_str)
    logger.info(f'Created the {utype} concat file at "{output}"')


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
    ### terms = f'ffmpeg -i "{file}" -vf setpts={1/timelapse_args.speed_factor}*PTS -c:v libx265 -r {timelapse_args.output_fps} -an "{output}"'

    # # Testing
    # terms = (
    #     f'ffmpeg -ss {cut_in} -i "{file}" '
    #     f"-vf setpts={1/timelapse_args.speed_factor}*PTS -c:v libx265 -r {timelapse_args.output_fps} -an "
    #     f'-vf "fade=t=in:st={fade_in_start}:d={fade_in},fade=t=out:st={fade_out_start}:d={fade_out}" '
    #     f'-t {cut_out} "{output}"'
    # )

    ### Building the terms string based on inputs
    terms = "ffmpeg "
    # Get durations
    durations = getClipFadeTime(file, 5, 20, 3, 3)
    # Add the beginning cut
    if durations["cut_in"] > 0:
        terms += f'-ss {durations["cut_in"]} '
    # Add the input file
    terms += f'-i "{file}" '
    # Add the vf
    if (
        durations["fade_in_l"] > 0
        or durations["fade_out_l"] > 0
        or timelapse_args.speed_factor != 0
    ):
        terms += f'-vf "'
        # Add the fade in if there is one
        if durations["fade_in_l"] > 0:
            terms += f"fade=t=in:st="
            # If we start the fade later start it then if not do it at the beginning
            if durations["fade_in_s"] > 0:
                terms += f'{durations["fade_in_s"]}:'
            else:
                terms += f"0:"
            terms += f'd:{durations["fade_in_l"]},'
        # Add the fade out if there is one
        if durations["fade_out_l"] > 0:
            terms += (
                f'fade=t=out:st={durations["fade_out_s"]}:d={durations["fade_out_l"]},'
            )
        # Add the speed up factor
        if timelapse_args.speed_factor != 0:
            terms += f'setpts={1/timelapse_args.speed_factor}*PTS" '
        # Replace the last character if there isn't a speed factor to close off the vf section
        else:
            terms = terms[:-1]
            terms += f'"'
    # Add the codec
    terms += f"-c:v libx265 "
    # Add the new framerate
    if timelapse_args.output_fps > 0:
        terms += f"-r {timelapse_args.output_fps} -an "
    else:
        terms += f"-an "
    # Add the trim
    if durations["cut_out"] > 0:
        terms += f'-t {durations["cut_out"]} "{output}"'
    else:
        terms += f'"{output}"'
    print(terms)
    input()
    # Run ffmpeg
    timelapse = subprocess.Popen(
        terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    timelapse.wait()


# Function to create the timelapse and the log info
def logTimelapses(video: pathlib.Path, output: pathlib.Path) -> None:
    # Create the new timelapse
    logger.info(f'Creating new timelapse of "{video}" at "{output}"')
    start = time.perf_counter()
    timelapseVideo(video)
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created a timelapse of "{video}" after {duration} seconds'
    )


# Function to delete a file and log the info
def delLog(file: pathlib.Path, notice1: str, notice2: str) -> None:
    logger.info(f'{notice1} "{file}"')
    os.remove(file)
    logger.info(f'{notice2} "{file}"')


# Function to create timelapses
def createTimelapses(video_files: list) -> None:
    # Turn every video into a timelapse
    for video in video_files:
        # Check if a timelapse already exists
        output = pathlib.Path.joinpath(timelapse_args.temp_directory, video.name)
        if checkPath(output):
            # Delete the existing file if that setting is enabled
            if timelapse_args.override_temp_video:
                delLog(
                    output,
                    "Deleting existing temp video",
                    "Deleted existing temp video",
                )
                # Create the new timelapse
                logTimelapses(video, output)
        # If the file doesn't exist just create it
        else:
            # Create the new timelapse
            logTimelapses(video, output)
        # Delete the source video file if that setting is enabled
        if timelapse_args.delete_video:
            delLog(
                video, "Deleting existing source video", "Deleted existing source video"
            )


# Function to combine the timelapse videos
def combineTimelapse(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" -c copy "{output_file}"'
    timelapse = subprocess.Popen(
        terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    timelapse.wait()


# Function to create the combined timelapse and log
def logCombineTimelapse(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    logger.info(f'Creating the new output timelapse at "{output_file}"')
    start = time.perf_counter()
    combineTimelapse(concat_file, output_file)
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created the new output timelapse at "{output_file}" after {duration} seconds'
    )


# Function to create the combined video timelapse
def createCombinedTimelapse(video_files: list):
    concat_video = pathlib.Path.joinpath(timelapse_args.temp_directory, "video.txt")
    concatFile(video_files, concat_video, "video")
    # Check if a output timelapse already exists
    output = pathlib.Path.joinpath(timelapse_args.output_directory, "timelapse.mp4")
    if checkPath(output):
        # Delete the existing output video file if that setting is enabled
        if timelapse_args.override_output:
            delLog(
                output,
                "Deleting existing output video",
                "Deleted existing output video",
            )
            # Create the timelapse
            logCombineTimelapse(concat_video, output)
    # If the file doesn't exist (duplicate code :pained_emoji:)
    else:
        # Create the timelapse
        logCombineTimelapse(concat_video, output)
    # Delete the temporary video files if that setting is enabled
    if not timelapse_args.keep_temp_video:
        logger.info(f"Deleting all the temp videos")
        # Doing this 1 by 1 instead of using shutil
        for file in video_files:
            delLog(
                file,
                "Deleting the temp video at",
                "Deleted the temp video at",
            )
        logger.info(f"Deleted all the temp videos")
    # Remove the video concat file
    delLog(
        concat_video,
        "Deleting the video concat file at",
        "Deleted the video concat file at",
    )


# Function to combine the audio
def combineAudio(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    # Merge the audio files
    audio_terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" -c:a "{output_file}"'
    audio_combine = subprocess.Popen(
        audio_terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    audio_combine.wait()


# Function to create the combined audio and log
def logCombineAudio(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    # Create the audio for the timelapse
    logger.info(f'Creating the new audio for the timelapse at "{output_file}"')
    start = time.perf_counter()
    combineTimelapse(concat_file, output_file)
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created the new audio for the timelapse at "{output_file}" after {duration} seconds'
    )


# Function to create the combined audio files
def createCombinedAudio(audio_files: list):
    # Path for the audio concat file
    audio_concat = pathlib.Path.joinpath(timelapse_args.temp_directory, "audio.txt")
    # Path for the outputted merged audio
    audio_out = pathlib.Path.joinpath(timelapse_args.output_directory, "audio.wav")
    # Creating the concat file
    concatFile(audio_files, audio_concat, "audio")
    # Check if a output audio already exists
    if checkPath(audio_out):
        # Delete the existing output audio file if that setting is enabled
        if timelapse_args.override_output:
            delLog(
                audio_out,
                "Deleting existing output audio",
                "Deleting existing output audio",
            )
            # Create the audio for the timelapse
            logCombineAudio(audio_concat, audio_out)
    # If the file doesn't exist (duplicate code :pained_emoji:)
    else:
        # Create the audio for the timelapse
        logCombineAudio(audio_concat, audio_out)
    # Delete the temp audio files if that setting is enabled
    if not timelapse_args.keep_temp_audio:
        logger.info(f"Deleting the temp audio")
        # Doing this 1 by 1 instead of using shutil
        for file in audio_files:
            delLog(
                file,
                "Deleting the temp audio at",
                "Deleted the temp audio at",
            )
        logger.info(f"Deleted the temp audio files")
    # Remove the audio file
    delLog(
        audio_concat,
        "Deleting the audio concat file at",
        "Deleted the audio concat file at",
    )


# Function to get the fade times
def getClipFadeTime(
    file: pathlib.Path,
    cut_in: float,
    cut_out: float,
    fade_in_l: float,
    fade_out_l: float,
) -> dict:
    # Get the length of the file
    duration = getLength(file)
    # Cutting stuff
    if cut_out == 0:
        new_duration = duration
    else:
        new_duration = cut_out
    # Get the fade times
    fade_in_s = cut_in
    fade_out_s = new_duration - fade_out_l
    return {
        "cut_in": cut_in,
        "cut_out": cut_out,
        "fade_in_l": fade_in_l,
        "fade_out_l": fade_out_l,
        "fade_in_s": fade_in_s,
        "fade_out_s": fade_out_s,
    }


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
    # Default is 30, because 60fps for an art timelapse is overkill
)
parser.add_argument(
    "-sf",
    "--speed_factor",
    help="How much do you want to speed up the timelapse by",
    type=float,
    default=30,
    # Default is 30 because that's 1 frame per seconds (assuming 30fps video)
)
parser.add_argument(
    "-ve",
    "--verbose",
    help="Displays in detail the step the program is doing",
    action="store_true",
)

cli_args = parser.parse_args()
print(cli_args)

## Get the command line arguments
timelapse_args = getPaths()

# Call the root logger basicConfig
logging.basicConfig()
# Create root logger
logging.root.setLevel(logging.NOTSET)
# Can do this instead of the above 2
# logging.basicConfig(level=logging.NOTSET)

# Creating logger for this module
# logger = logging.getLogger(__name__)
logger = logging.getLogger("Timelapse")
# If the verbose option is passed set the logger level to info
if timelapse_args.verbose:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.WARNING)

# Get the files
video_files = getFiles(timelapse_args.video_directory, [".mp4", ".mkv"])
audio_files = getFiles(timelapse_args.audio_directory, [".wav", ".mp3"])

# Check if there are videos in the video directory
if len(video_files) == 0:
    logger.critical("There are no videos in the video file")
    sys.exit()

# Create timelapses
createTimelapses(video_files)

# Create a concat list of all the videos
timelapse_video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
timelapse_audio_files = getFiles(timelapse_args.temp_directory, [".wav", ".mp3"])


# Creating the concat of the timelapse videos
createCombinedTimelapse(timelapse_video_files)

# Merge audio files if there are audio files (NOTE: Add transition later)
if len(audio_files) != 0:
    # Create the modified audio files
    #####
    # Create the combined audio files
    createCombinedAudio(timelapse_audio_files)

    ############

    # Add the audio to the video (make sure the combined audio is longer than the video, it will use the shortest)
    video_out = pathlib.Path.joinpath(timelapse_args.output_directory, "timelapse.mp4")
    video_out_audio = pathlib.Path.joinpath(
        timelapse_args.output_directory, "timelapse_audio.mp4"
    )
    # Check if a output audio already exists
    if checkPath(video_out_audio):
        # Delete the existing output video with audio file if that setting is enabled
        if timelapse_args.override_output:
            logger.info(
                f'Deleting existing output video with audio "{video_out_audio}"'
            )
            os.remove(video_out_audio)
            logger.info(f'Deleted existing output video with audio "{video_out_audio}"')
            # Create the video with audio
            vide_audio_terms = f'ffmpeg -i "{video_out}" -i "{audio_out}" -map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
            add_audio = subprocess.Popen(
                vide_audio_terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            # Create the timelapse
            logger.info(f'Creating the timelapse with audio at "{video_out_audio}"')
            start = time.perf_counter()
            # Run the command and wait for it to finish
            add_audio.wait()
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully created the timelapse with audio at "{video_out_audio}" after {duration} seconds'
            )
    # If the file doesn't exist (duplicate code :pained_emoji:)
    else:
        # Create the video with audio
        vide_audio_terms = f'ffmpeg -i "{video_out}" -i "{audio_out}" -map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
        add_audio = subprocess.Popen(
            vide_audio_terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # Create the timelapse
        logger.info(f'Creating the timelapse with audio at "{video_out_audio}"')
        start = time.perf_counter()
        # Run the command and wait for it to finish
        add_audio.wait()
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully created the timelapse with audio at "{video_out_audio}" after {duration} seconds'
        )


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
