# Header Comment
# Project: [Art Timelapse Maker] [https://github.com/GreenBeanio/Art-Timelapse-Maker]
# Copyright: Copyright (c) [2024]-[2024] [Art Timelapse Maker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to create timelapses from videos.]
# File Description: [Creates timelapses from videos (specifically for art, but can be used for any purpose).]

# Imports
import os
import pathlib
import subprocess
import sys
import argparse
import logging
from typing import List, Tuple, Dict, Union
import time
import json
import datetime
import random

# Recording the starting time just for fun
total_start = time.perf_counter()


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
        audio_speed_factor,
        prompt,
        video_clip_in,
        video_clip_out,
        video_fade_in,
        video_fade_out,
        audio_clip_in,
        audio_clip_out,
        audio_fade_in,
        audio_fade_out,
        output_video_fade_in,
        output_video_fade_out,
        output_audio_fade_in,
        output_audio_fade_out,
        keep_unfaded_video,
        keep_unfaded_audio,
        compression_level,
        resize,
        settings_directory,
        use_settings,
        override_settings,
        clear_settings,
        delete_settings,
        threads,
        randomize_audio,
        randomize_video,
        override_source_path,
        preserve_audio,
        modified_output_video_fade_in,
        modified_output_video_fade_out,
        modified_output_audio_fade_in,
        modified_output_audio_fade_out,
        image_length,
        dont_save_settings,
        width,
        height,
        use_custom_order,
        override_custom_order,
        clear_custom_order,
        delete_custom_order,
        dont_save_custom_order,
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
        self.audio_speed_factor = audio_speed_factor
        self.prompt = prompt
        self.video_clip_in = video_clip_in
        self.video_clip_out = video_clip_out
        self.video_fade_in = video_fade_in
        self.video_fade_out = video_fade_out
        self.audio_clip_in = audio_clip_in
        self.audio_clip_out = audio_clip_out
        self.audio_fade_in = audio_fade_in
        self.audio_fade_out = audio_fade_out
        self.output_video_fade_in = output_video_fade_in
        self.output_video_fade_out = output_video_fade_out
        self.output_audio_fade_in = output_audio_fade_in
        self.output_audio_fade_out = output_audio_fade_out
        self.keep_unfaded_video = keep_unfaded_video
        self.keep_unfaded_audio = keep_unfaded_audio
        self.compression_level = compression_level
        self.resize = resize
        self.settings_directory = settings_directory
        self.use_settings = use_settings
        self.override_settings = override_settings
        self.clear_settings = clear_settings
        self.delete_settings = delete_settings
        self.threads = threads
        self.randomize_audio = randomize_audio
        self.randomize_video = randomize_video
        self.override_source_path = override_source_path
        self.preserve_audio = preserve_audio
        self.modified_output_video_fade_in = modified_output_video_fade_in
        self.modified_output_video_fade_out = modified_output_video_fade_out
        self.modified_output_audio_fade_in = modified_output_audio_fade_in
        self.modified_output_audio_fade_out = modified_output_audio_fade_out
        self.image_length = image_length
        self.dont_save_settings = dont_save_settings
        self.width = width
        self.height = height
        self.use_custom_order = use_custom_order
        self.override_custom_order = override_custom_order
        self.clear_custom_order = clear_custom_order
        self.delete_custom_order = delete_custom_order
        self.dont_save_custom_order = dont_save_custom_order


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


# Function to get the paths to use (and verify the inputs)
def getPaths() -> userArguments:
    # Bool to store if all arguments are valid or not
    valid_arguments = True
    # Get the directory where the script was called from
    cwd = pathlib.Path().resolve()
    # Getting the video directory
    if cli_args.video_directory is None:
        video_source_directory = pathlib.Path.joinpath(cwd, "video")
        createDir(video_source_directory)
    else:
        if checkPath(cli_args.video_directory):
            video_source_directory = cli_args.video_directory
        else:
            logger.critical("Invalid video source directory")
            valid_arguments = False
    # Getting the audio directory
    if cli_args.audio_directory is None:
        audio_source_directory = pathlib.Path.joinpath(cwd, "audio")
        createDir(audio_source_directory)
    else:
        if checkPath(cli_args.audio_directory):
            audio_source_directory = cli_args.audio_directory
        else:
            logger.critical("Invalid audio source directory")
            valid_arguments = False
    # Getting the output directory
    if cli_args.output_directory is None:
        output_directory = pathlib.Path.joinpath(cwd, "output")
        createDir(output_directory)
    else:
        if checkPath(cli_args.output_directory):
            output_directory = cli_args.output_directory
        else:
            logger.critical("Invalid output directory")
            valid_arguments = False
    # Getting the temp directory
    if cli_args.temp_directory is None:
        temp_directory = pathlib.Path.joinpath(cwd, "temp")
        createDir(temp_directory)
    else:
        if checkPath(cli_args.temp_directory):
            temp_directory = cli_args.temp_directory
        else:
            logger.critical("Invalid temp directory")
            valid_arguments = False
    # Getting the settings directory
    if cli_args.settings_directory is None:
        settings_directory = pathlib.Path.joinpath(cwd, "settings")
        createDir(settings_directory)
    else:
        if checkPath(cli_args.settings_directory):
            settings_directory = cli_args.settings_directory
        else:
            logger.critical("Invalid temp directory")
            valid_arguments = False

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
    verbose = cli_args.verbose
    prompt = cli_args.prompt
    keep_unfaded_video = cli_args.keep_unfaded_video
    keep_unfaded_audio = cli_args.keep_unfaded_audio
    use_settings = cli_args.use_settings
    override_settings = cli_args.override_settings
    clear_settings = cli_args.clear_settings
    delete_settings = cli_args.delete_settings
    randomize_audio = cli_args.randomize_audio
    randomize_video = cli_args.randomize_video
    override_source_path = cli_args.override_source_path
    preserve_audio = cli_args.preserve_audio
    dont_save_settings = cli_args.dont_save_settings
    use_custom_order = cli_args.use_custom_order
    override_custom_order = cli_args.override_custom_order
    clear_custom_order = cli_args.clear_custom_order
    delete_custom_order = cli_args.delete_custom_order
    dont_save_custom_order = cli_args.dont_save_custom_order

    # Validating other inputs
    if cli_args.output_fps > 0:
        output_fps = cli_args.output_fps
    else:
        logger.critical(
            "Invalid fps: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.speed_factor >= 0:
        speed_factor = cli_args.speed_factor
    else:
        logger.critical(
            "Invalid speed factor: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if (
        cli_args.audio_speed_factor >= 0.5 and cli_args.audio_speed_factor <= 100
    ) or cli_args.audio_speed_factor == 0:
        audio_speed_factor = cli_args.audio_speed_factor
    else:
        logger.critical(
            "Invalid audio speed factor: Must be a float equal to or greater than 0.5 and less than 100, or 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.video_clip_in >= 0:
        video_clip_in = cli_args.video_clip_in
    else:
        logger.critical(
            "Invalid video clip in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.video_clip_out >= 0:
        video_clip_out = cli_args.video_clip_out
    else:
        logger.critical(
            "Invalid video clip out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.video_fade_in >= 0:
        video_fade_in = cli_args.video_fade_in
    else:
        logger.critical(
            "Invalid video fade in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.video_fade_out >= 0:
        video_fade_out = cli_args.video_fade_out
    else:
        logger.critical(
            "Invalid video fade out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.audio_clip_in >= 0:
        audio_clip_in = cli_args.audio_clip_in
    else:
        logger.critical(
            "Invalid audio clip in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.audio_clip_out >= 0:
        audio_clip_out = cli_args.audio_clip_out
    else:
        logger.critical(
            "Invalid audio clip out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.audio_fade_in >= 0:
        audio_fade_in = cli_args.audio_fade_in
    else:
        logger.critical(
            "Invalid audio fade in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.audio_fade_out >= 0:
        audio_fade_out = cli_args.audio_fade_out
    else:
        logger.critical(
            "Invalid audio fade out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.output_video_fade_in >= 0:
        output_video_fade_in = cli_args.output_video_fade_in
    else:
        logger.critical(
            "Invalid output video fade in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.output_video_fade_out >= 0:
        output_video_fade_out = cli_args.output_video_fade_out
    else:
        logger.critical(
            "Invalid output video fade out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.output_audio_fade_in >= 0:
        output_audio_fade_in = cli_args.output_audio_fade_in
    else:
        logger.critical(
            "Invalid output audio fade in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.output_audio_fade_out >= 0:
        output_audio_fade_out = cli_args.output_audio_fade_out
    else:
        logger.critical(
            "Invalid output audio fade out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if (
        cli_args.compression_level >= 0 and cli_args.compression_level <= 52
    ) or cli_args.compression_level == -1:
        compression_level = cli_args.compression_level
    else:
        logger.critical(
            "Invalid compression: Must be an integer between 0 and 51, ffmpeg range is 0 to 51 with a default of 23 (lower is better quality, 0 is lossless). Passing -1 will disable this option (default)"
        )
        valid_arguments = False
    if cli_args.resize >= 0:
        resize = cli_args.resize
    else:
        logger.critical(
            "Invalid resize: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.threads >= -1:
        threads = cli_args.threads
    else:
        logger.critical(
            "Invalid threads: Must be an integer equal to or greater than -1. -1 will disable this option (default), 0 is the optimal amount determined by ffmpeg, and any positive integer is the passed amount of threads."
        )
        valid_arguments = False
    if cli_args.modified_output_video_fade_in >= 0:
        modified_output_video_fade_in = cli_args.modified_output_video_fade_in
    else:
        logger.critical(
            "Invalid modified output video fade in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.modified_output_video_fade_out >= 0:
        modified_output_video_fade_out = cli_args.modified_output_video_fade_out
    else:
        logger.critical(
            "Invalid modified output video fade out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.modified_output_audio_fade_in >= 0:
        modified_output_audio_fade_in = cli_args.modified_output_audio_fade_in
    else:
        logger.critical(
            "Invalid modified output audio fade in: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.modified_output_audio_fade_out >= 0:
        modified_output_audio_fade_out = cli_args.modified_output_audio_fade_out
    else:
        logger.critical(
            "Invalid modified output audio fade out: Must be a float equal to or greater than 0. 0 to disable (default)."
        )
        valid_arguments = False
    if cli_args.image_length >= (1 / cli_args.output_fps):
        image_length = cli_args.image_length
    else:
        logger.critical(
            f"Invalid image length: Default image length must be larger than 1 output frame length ({1/cli_args.output_fps} seconds at the output fps)"
        )
    if cli_args.width > 0:
        width = cli_args.width
    else:
        logger.critical("Invalid width: Must be an integer greater than 0.")
        valid_arguments = False
    if cli_args.height > 0:
        height = cli_args.height
    else:
        logger.critical("Invalid height: Must be an integer greater than 0.")
        valid_arguments = False

    # Close application if inputs aren't valid
    if not valid_arguments:
        logger.critical("Fix problematic arguments!")
        sys.exit()

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
        audio_speed_factor,
        prompt,
        video_clip_in,
        video_clip_out,
        video_fade_in,
        video_fade_out,
        audio_clip_in,
        audio_clip_out,
        audio_fade_in,
        audio_fade_out,
        output_video_fade_in,
        output_video_fade_out,
        output_audio_fade_in,
        output_audio_fade_out,
        keep_unfaded_video,
        keep_unfaded_audio,
        compression_level,
        resize,
        settings_directory,
        use_settings,
        override_settings,
        clear_settings,
        delete_settings,
        threads,
        randomize_audio,
        randomize_video,
        override_source_path,
        preserve_audio,
        modified_output_video_fade_in,
        modified_output_video_fade_out,
        modified_output_audio_fade_in,
        modified_output_audio_fade_out,
        image_length,
        dont_save_settings,
        width,
        height,
        use_custom_order,
        override_custom_order,
        clear_custom_order,
        delete_custom_order,
        dont_save_custom_order,
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
def concatFile(
    files_d: Dict[int, pathlib.Path], output: pathlib.Path, utype: bool
) -> None:
    # Grab just the values from the dict
    files = files_d.values()
    # What type of file it is and randomizing if needed
    if utype:
        ustr = "video"
        if timelapse_args.randomize_video:
            random.shuffle(files)
    else:
        ustr = "audio"
        if timelapse_args.randomize_audio:
            random.shuffle(files)
    logger.info(f'Creating the {ustr} concat file at "{output}"')
    # New list to actually use
    temp_str = ""
    for file in files:
        # Replace apostrophes in the file with the escape sequence ffmpeg needs
        # file_string = str(file.resolve().absolute())
        file_string = str(file.resolve())
        file_string = file_string.replace("'", "'\\''")
        temp_str += f"file '{file_string}'\n"
    with open(output, "w+") as file:
        file.write(temp_str)
    logger.info(f'Created the {ustr} concat file at "{output}"')


# Function to use ffprobe to get the length of the file
def getLength(file: pathlib.Path) -> float:
    terms = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file}"'
    ffprobe = subprocess.Popen(
        terms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # Run the command and get the result
    duration, err = ffprobe.communicate()
    return float(duration)


# Function to use ffprobe to get the resolution of a file
def getResolution(file: pathlib.Path) -> Tuple[int, int]:
    terms = f'ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0:s=x "{file}"'
    ffprobe = subprocess.Popen(
        terms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # Run the command and get the result
    resolution, err = ffprobe.communicate()
    resolution = resolution.split("x")
    resolution[1] = resolution[1].strip("\n")
    return (int(resolution[0]), int(resolution[1]))


# Function to get the framerate of the file
def getFramerate(file: pathlib.Path) -> float:
    terms = f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "{file}"'
    ffprobe = subprocess.Popen(
        terms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # Run the command and get the result
    result, err = ffprobe.communicate()
    terms = result.split("/")
    framerate = round(float(int(terms[0]) / int(terms[1])), 2)
    return framerate


# Function to run FFmpeg
def runFFmpeg(terms: str) -> None:
    timelapse = subprocess.Popen(
        terms, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    # Run the command and wait for it to finish
    timelapse.wait()


# Function to create a timelapse from a video
def timelapseVideo(
    file: pathlib.Path,
    final_output: pathlib.Path,
    speed_factor: float,
    cut_in: float,
    cut_out: float,
    cut_from_end: bool,
    fade_in: float,
    fade_out: float,
) -> None:
    # Variables for handling the current process
    current_input = file
    ## FFmpeg is a little fucky so I think I have to do these in multiple steps

    # Check if the file needs no modification
    if not (
        (cut_in != 0 or cut_out != 0)
        or (speed_factor != 0 and speed_factor != 1)
        or (fade_in != 0 or fade_out != 0)
    ):
        # All we need to do is change the codec and the framerate to match the rest of the videos
        terms = f'ffmpeg -i "{file}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        terms += f'-vf "{resize_vf}" -c:v libx265 -r {timelapse_args.output_fps} '
        # If we're not preserving the audio
        if not timelapse_args.preserve_audio:
            terms += f"-an "
        # If we are preserving the audio
        else:
            terms += f"-c:a mp3 "
        # Output
        terms += f'"{final_output}"'
        # Run ffmpeg
        runFFmpeg(terms)
        # We can skip the rest of the function and save a whopping 3 conditionals.
        return

    # Bool to not delete if getting the source
    first = True

    # FFmpeg clip the video
    if cut_in != 0 or cut_out != 0:
        logger.info(f'Clipping the temp timelapse of "{file}"')
        start = time.perf_counter()
        # Get durations
        cut_duration = getClipTime(current_input, cut_in, cut_out, cut_from_end, False)
        terms = "ffmpeg "
        # Add the beginning cut
        if cut_duration["cut_in"] != 0:
            terms += f'-ss {cut_duration["cut_in"]} '
        # Add the input file
        terms += f'-i "{file}" '
        # Compare the resolutions
        match_resolution = checkResolution(file)
        if not match_resolution:
            terms += f'-vf "{resize_vf}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Check other possibilities to see what output to use
        if (fade_in != 0 or fade_out != 0) or (speed_factor != 1 and speed_factor != 0):
            temp_file = f"{file.stem}c{file.suffix}"
            output = pathlib.Path.joinpath(timelapse_args.temp_directory, temp_file)
            # Copy the video codec and remove audio
            if match_resolution:
                terms += f"-c:v copy "  # Not sure if copy will still work if resizing will need to test
            else:
                terms += f"-c:v libx265 "  # I couldn't copy it anymore ... oh well
            # If we're not preserving the audio
            if not timelapse_args.preserve_audio:
                terms += f"-an "
            # If we are preserving the audio check the speed factor to speed up audio too
            #  or else it'll just freeze on the last frame
            elif speed_factor != 1 and speed_factor != 0:
                tempo = generateTempo(speed_factor)
                terms += f'-c:a mp3 -af "{tempo}"'
            # If not using the speed factor either
            else:
                terms += f"-c:a mp3 "
            # Add the trim
            if cut_duration["cut_out"] != 0:
                terms += f'-t {cut_duration["new_duration"]} "{output}"'
            else:
                terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save 2 conditionals :pain:)
            runFFmpeg(terms)
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully clipped the temp timelapse of "{file} after {duration} seconds'
            )
            # Set first to false
            first = False
        else:
            # Change the video codec, change the framerate, and remove audio (We need to do this here, but not if
            # another process is being done. This is because we need to do it at some point, but clipping is really
            # fast if we don't change the codec or framerate.)
            terms += f"-c:v libx265 -r {timelapse_args.output_fps} "
            # If we're not preserving the audio
            if not timelapse_args.preserve_audio:
                terms += f"-an "
            # If we are preserving the audio
            else:
                terms += f"-c:a mp3 "
            output = final_output
            # Add the trim
            if cut_duration["cut_out"] != 0:
                terms += f'-t {cut_duration["new_duration"]} "{output}"'
            else:
                terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save 2 conditionals :pain:)
            runFFmpeg(terms)
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully clipped the temp timelapse of "{file} after {duration} seconds'
            )
            return

    # FFmpeg speed up the video
    if speed_factor != 0 and speed_factor != 1:
        logger.info(f'Speeding up the temp timelapse of "{file}"')
        start = time.perf_counter()
        terms = "ffmpeg "
        # Add the input file and speed up factor
        terms += f'-i "{current_input}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        terms += f'-vf "{resize_vf},setpts={1/speed_factor}*PTS" '
        # Check other possibilities to see what output to use
        if fade_in != 0 or fade_out != 0:
            temp_file = f"{file.stem}s{file.suffix}"
            output = pathlib.Path.joinpath(timelapse_args.temp_directory, temp_file)
            # Remove audio (have to add the codec or it doesn't work, copying it doesn't work)
            terms += f"-c:v libx265 "
            # If we're not preserving the audio
            if not timelapse_args.preserve_audio:
                terms += f"-an "
            # If we are preserving the audio
            else:
                terms += f"-c:a mp3 "
            # Output
            terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save a conditional :pain:)
            runFFmpeg(terms)
            # Remove if not getting from source (getting from temporary)
            if not first:
                os.remove(current_input)
            else:
                first = False
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully sped the temp timelapse of "{file} after {duration} seconds'
            )
        else:
            output = final_output
            # Remove audio (have to add the codec or it doesn't work, copying it doesn't work)
            terms += f"-c:v libx265 -r {timelapse_args.output_fps} "
            # If we're not preserving the audio
            if not timelapse_args.preserve_audio:
                terms += f"-an "
            # If we are preserving the audio
            else:
                terms += f"-c:a mp3 "
            # Output
            terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save a conditional :pain:)
            runFFmpeg(terms)
            # Remove if not getting from source (getting from temporary)
            if not first:
                os.remove(current_input)
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully sped the temp timelapse of "{file} after {duration} seconds'
            )
            return

    # FFmpeg fade the video
    if fade_in != 0 or fade_out != 0:
        logger.info(f'Fading the temp timelapse of "{file}"')
        start = time.perf_counter()
        # Get durations
        fade_duration = getFadeTime(current_input, fade_in, fade_out)
        terms = f'ffmpeg -i "{current_input}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the fades
        terms += f'-vf "{resize_vf},'
        # Add the fade in if there is one
        if fade_duration["fade_in_l"] != 0:
            terms += f'fade=t=in:st=0:d={fade_duration["fade_in_l"]},'
        # Add the fade out if there is one
        if fade_duration["fade_out_l"] != 0:
            terms += f'fade=t=out:st={fade_duration["fade_out_s"]}:d={fade_duration["fade_out_l"]}"'
        # If there isn't a fade out replace the comma with a double quote
        else:
            terms = terms[:-1]
            terms += f'"'
        # Copy the video codec and remove audio.
        terms += f" -c:v libx265 -r {timelapse_args.output_fps} "
        # If we're not preserving the audio
        if not timelapse_args.preserve_audio:
            terms += f"-an "
        # If we are preserving the audio
        else:
            terms += f"-c:a mp3 "
        # Output
        terms += f'"{final_output}"'
        # Run ffmpeg
        runFFmpeg(terms)
        # Remove if not getting from source (getting from temporary)
        if not first:
            os.remove(current_input)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully faded the temp timelapse of "{file} after {duration} seconds'
        )
        return  # It would return after this either way, but whatever


# Function to create the timelapse and the log info
def logTimelapses(video: pathlib.Path, output: pathlib.Path, index: int) -> None:
    # Create the new timelapse
    logger.info(f'Creating new timelapse of "{video}" at "{output}"')
    start = time.perf_counter()
    timelapseVideo(
        video,
        output,
        user_answers[video][index]["speed_factor"],
        user_answers[video][index]["clip_in"],
        user_answers[video][index]["clip_out"],
        user_answers[video][index]["clip_from_end"],
        user_answers[video][index]["fade_in"],
        user_answers[video][index]["fade_out"],
    )
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created a timelapse of "{video}" after {duration} seconds'
    )


# Function to delete a file and log the info
def delLog(file: pathlib.Path, notice1: str, notice2: str) -> None:
    try:
        logger.info(f'{notice1} "{file}"')
        if os.path.exists(file):
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                os.rmdir(file)
            logger.info(f'{notice2} "{file}"')
        else:
            logger.info(f'Tried to delete "{file}" but it doesn\t exist')
    except:
        logger.warning(f'Couldn\'t delete at "{file}"')


# Function to create multiple timelapses
def createTimelapses(video_files: list):
    # Turn every video into a timelapse
    for video in video_files:
        video_settings = user_answers[video]
        # For every clip we're making for that file
        # for index, clips in enumerate(video_settings):
        for index in range(len(video_settings)):
            # Creating the new output
            output = pathlib.Path.joinpath(
                timelapse_args.temp_directory, f"{video.stem}_{index}{video.suffix}"
            )
            # Check if a timelapse already exists
            if checkPath(output):
                # Delete the existing file if that setting is enabled
                if timelapse_args.override_temp_video:
                    delLog(
                        output,
                        "Deleting existing temp video",
                        "Deleted existing temp video",
                    )
                    # Create the new timelapse
                    logTimelapses(video, output, index)
            # If the file doesn't exist just create it
            else:
                # Create the new timelapse
                logTimelapses(video, output, index)
        # Delete the source video file if that setting is enabled
        if timelapse_args.delete_video:
            delLog(
                video, "Deleting existing source video", "Deleted existing source video"
            )


# Function to combine the timelapse videos
def combineTimelapse(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    # Check if using a fade on the output
    if (
        timelapse_args.output_video_fade_in != 0
        or timelapse_args.output_video_fade_out != 0
    ):
        # Temporary path
        temp_out = pathlib.Path.joinpath(
            timelapse_args.output_directory, "timelapse_plain.mp4"
        )
        logger.info(f'Creating the unfaded output timelapse "{temp_out}"')
        start = time.perf_counter()
        # Create the combined timelapse
        terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        terms += f"-c:v libx265 -r {timelapse_args.output_fps} "
        # If we're not preserving the audio
        if not timelapse_args.preserve_audio:
            terms += f"-an "
        # If we are preserving the audio
        else:
            terms += f"-c:a mp3 "
        # Output
        terms += f'"{temp_out}"'
        runFFmpeg(terms)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Created the unfaded output timelapse "{temp_out}" after {duration} seconds'
        )
        # Create the fade
        logger.info(f'Fading the output timelapse "{output_file}"')
        start = time.perf_counter()
        # Get durations
        fade_duration = getFadeTime(
            temp_out,
            timelapse_args.output_video_fade_in,
            timelapse_args.output_video_fade_out,
        )
        terms = f'ffmpeg -i "{temp_out}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the fades
        terms += f'-vf "{resize_vf},'
        # Add the fade in if there is one
        if fade_duration["fade_in_l"] != 0:
            terms += f'fade=t=in:st=0:d={fade_duration["fade_in_l"]},'
        # Add the fade out if there is one
        if fade_duration["fade_out_l"] != 0:
            terms += f'fade=t=out:st={fade_duration["fade_out_s"]}:d={fade_duration["fade_out_l"]}"'
        # If there isn't a fade out replace the comma with a double quote
        else:
            terms = terms[:-1]
            terms += f'"'
        # Copy the video codec and remove audio.
        terms += f" -c:v libx265 -r {timelapse_args.output_fps} "
        # If we're not preserving the audio
        if not timelapse_args.preserve_audio:
            terms += f"-an "
        # If we are preserving the audio
        else:
            terms += f"-c:a mp3 "
        # Output
        terms += f'"{output_file}"'
        # Run ffmpeg
        runFFmpeg(terms)
        # Remove if not getting from source (getting from temporary)
        if not timelapse_args.keep_unfaded_video:
            os.remove(temp_out)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully faded the output timelapse "{output_file}" after {duration} seconds'
        )
    # If not using a fade just output it
    else:
        # Merge the timelapse files
        terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" -vf "{resize_vf}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        terms += f"-c:v libx265 -r {timelapse_args.output_fps} "
        # If we're not preserving the audio
        if not timelapse_args.preserve_audio:
            terms += f"-an "
        # If we are preserving the audio
        else:
            terms += f"-c:a mp3 "
        # Output
        terms += f'"{output_file}"'
        runFFmpeg(terms)


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
    concatFile(video_order, concat_video, True)
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


# Function to generate audio tempo because it has limits
def generateTempo(speed: float) -> str:
    # Base string
    tempo = ""
    # Bool based on the speed
    # If we're making it slower we can't go less that 0.5
    if speed < 0.5:
        speed_type = False
    # If we're making it faster we can use up to 100, but going over 2 skips sounds
    elif speed > 2:
        speed_type = True
    # Variables to store the results
    new_speed = speed
    rounds = 0
    # Getting how many rounds we need to add
    while True:
        # Going faster
        if speed_type:
            new_speed = new_speed / 2
            rounds += 1
            if new_speed <= 2:
                # main = 2**rounds  # Wait even these are useless besides testing
                base = 2
                break
        # Going slower
        else:
            new_speed = new_speed / 0.5
            rounds += 1
            if new_speed >= 0.5:
                # main = 0.5**rounds  # Wait even these are useless besides testing
                base = 0.5
                break
    # Getting the remainder to multiply by (This is actually useless it justs recalculates the new speed value :cry:)
    # remainder = speed / main
    # new = main * remainder
    # Testing the final value (Wait even this is useless outside of testing :cry_again:)
    # last = main * new_speed
    # print(last == speed)
    for x in range(rounds):
        tempo += f"atempo={base},"
    # add the final atempo
    tempo += f"atempo={new_speed}"
    return tempo


# Function to modify an audio file
def timelapseAudio(
    file: pathlib.Path,
    final_output: pathlib.Path,
    speed_factor: float,
    cut_in: float,
    cut_out: float,
    cut_from_end: bool,
    fade_in: float,
    fade_out: float,
) -> None:
    # Variables for handling the current process
    current_input = file
    ## FFmpeg is a little fucky so I think I have to do these in multiple steps

    # Check if the file needs no modification
    if not (
        (cut_in != 0 or cut_out != 0)
        or (speed_factor != 0 and speed_factor != 1)
        or (fade_in != 0 or fade_out != 0)
    ):
        # All we need to do is change the codec to match the rest of the audio
        terms = f'ffmpeg -i "{file}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        terms += f'-c:a mp3 "{final_output}"'
        # Run ffmpeg
        runFFmpeg(terms)
        # We can skip the rest of the function and save a whopping 2 conditionals.
        return

    # Bool to not delete if getting the source
    first = True

    # FFmpeg clip the audio
    if cut_in != 0 or cut_out != 0:
        logger.info(f'Clipping the temp audio of "{file}"')
        start = time.perf_counter()
        # Get durations
        cut_duration = getClipTime(current_input, cut_in, cut_out, cut_from_end, False)
        terms = "ffmpeg "
        # Add the beginning cut
        if cut_duration["cut_in"] != 0:
            terms += f'-ss {cut_duration["cut_in"]} '
        # Check other possibilities to see what output to use
        if (fade_in != 0 or fade_out != 0) or (speed_factor != 0 and speed_factor != 1):
            # Add the input file (can copy codec on the trim)
            terms += f'-i "{file}" '
            # Add the threads
            if timelapse_args.threads != -1:
                terms += f"-threads {timelapse_args.threads} "
            # Add the rest of the terms
            terms += f"-c:a copy "
            temp_file = f"{file.stem}c{file.suffix}"
            output = pathlib.Path.joinpath(timelapse_args.temp_directory, temp_file)
            # Add the trim
            if cut_duration["cut_out"] != 0:
                terms += f'-t {cut_duration["new_duration"]} "{output}"'
            else:
                terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save 2 conditionals)
            runFFmpeg(terms)
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully clipped the temp audio of "{file} after {duration} seconds'
            )
            # Set first to false
            first = False
        else:
            # Add the input file (Need to change the codec since it wont be in another step)
            terms += f'-i "{file}" '
            # Add the threads
            if timelapse_args.threads != -1:
                terms += f"-threads {timelapse_args.threads} "
            # Add the rest of the terms
            terms += f"-c:a mp3 "
            output = final_output
            # Add the trim
            if cut_duration["cut_out"] != 0:
                terms += f'-t {cut_duration["new_duration"]} "{output}"'
            else:
                terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save 2 conditionals)
            runFFmpeg(terms)
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully clipped the temp audio of "{file} after {duration} seconds'
            )
            return

    # FFmpeg speed up the audio
    if speed_factor != 0 and speed_factor != 1:
        logger.info(f'Speeding up the temp audio of "{file}"')
        start = time.perf_counter()
        terms = "ffmpeg "
        # Add the input file and speed up factor (need to change codec)
        terms += f'-i "{current_input}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        tempo = generateTempo(speed_factor)
        terms += f'-af "{tempo}" -c:a mp3 '
        # Check other possibilities to see what output to use
        if fade_in != 0 or fade_out != 0:
            temp_file = f"{file.stem}s{file.suffix}"
            output = pathlib.Path.joinpath(timelapse_args.temp_directory, temp_file)
            # Remove audio (have to add the codec or it doesn't work, copying it doesn't work)
            terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save a conditional :pain:)
            runFFmpeg(terms)
            # Remove if not getting from source (getting from temporary)
            if not first:
                os.remove(current_input)
            else:
                first = False
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully sped the temp audio of "{file} after {duration} seconds'
            )
        else:
            output = final_output
            terms += f'"{output}"'
            # Run ffmpeg (duplicate code to save a conditional :pain:)
            runFFmpeg(terms)
            # Remove if not getting from source (getting from temporary)
            if not first:
                os.remove(current_input)
            current_input = output
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully sped the temp audio of "{file} after {duration} seconds'
            )
            return

    # FFmpeg fade the video
    if fade_in != 0 or fade_out != 0:
        logger.info(f'Fading the temp audio of "{file}"')
        start = time.perf_counter()
        # Get durations
        fade_duration = getFadeTime(current_input, fade_in, fade_out)
        terms = "ffmpeg "
        # Add the input file
        terms += f'-i "{current_input}" '
        # Add the threads
        if timelapse_args.threads != -1:
            terms += f"-threads {timelapse_args.threads} "
        # Add the fades
        terms += f'-af "'
        # Add the fade in if there is one
        if fade_duration["fade_in_l"] != 0:
            terms += f'afade=t=in:st=0:d={fade_duration["fade_in_l"]},'
        # Add the fade out if there is one
        if fade_duration["fade_out_l"] != 0:
            terms += f'afade=t=out:st={fade_duration["fade_out_s"]}:d={fade_duration["fade_out_l"]}"'
        # If there isn't a fade out replace the comma with a double quote
        else:
            terms = terms[:-1]
            terms += f'"'
        # Change the audio codec (can't seem to copy it if fading)
        terms += f' -c:a mp3 "{final_output}"'
        # Run ffmpeg
        runFFmpeg(terms)
        # Remove if not getting from source (getting from temporary)
        if not first:
            os.remove(current_input)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully faded the temp audio of "{file} after {duration} seconds'
        )
        return  # Useless return, but whatever


# Function to create the audio and the log info
def logAudio(audio: pathlib.Path, output: pathlib.Path, index: int) -> None:
    # Create the new timelapse
    logger.info(f'Creating modified audio of "{audio}" at "{output}"')
    start = time.perf_counter()
    timelapseAudio(
        audio,
        output,
        user_answers[audio][index]["speed_factor"],
        user_answers[audio][index]["clip_in"],
        user_answers[audio][index]["clip_out"],
        user_answers[audio][index]["clip_from_end"],
        user_answers[audio][index]["fade_in"],
        user_answers[audio][index]["fade_out"],
    )
    end = time.perf_counter()
    duration = end - start
    logger.info(f'Successfully modified audio of "{audio}" after {duration} seconds')


# Function to create audio (modify all the audio files)
def createAudio(audio_files: list) -> None:
    # Turn every video into a timelapse
    for audio in audio_files:
        audio_settings = user_answers[audio]
        for index in range(len(audio_settings)):
            # Creating the new output
            output = pathlib.Path.joinpath(
                timelapse_args.temp_directory, f"{audio.stem}_{index}{audio.suffix}"
            )
            # Check if a timelapse already exists
            if checkPath(output):
                # Delete the existing file if that setting is enabled
                if timelapse_args.override_temp_audio:
                    delLog(
                        output,
                        "Deleting existing temp audio",
                        "Deleted existing temp audio",
                    )
                    # Create the new timelapse
                    logAudio(audio, output, index)
            # If the file doesn't exist just create it
            else:
                # Create the new timelapse
                logAudio(audio, output, index)
        # Delete the source video file if that setting is enabled
        if timelapse_args.delete_audio:
            delLog(
                audio, "Deleting existing source audio", "Deleted existing source audio"
            )


# Function to combine the audio
def combineAudio(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    # Check if using a fade on the output
    if (
        timelapse_args.output_audio_fade_in != 0
        or timelapse_args.output_audio_fade_out != 0
    ):
        # Temporary path
        temp_out = pathlib.Path.joinpath(
            timelapse_args.output_directory, "audio_plain.wav"
        )
        logger.info(f'Creating the unfaded output audio "{temp_out}"')
        start = time.perf_counter()
        # Create the combined file
        audio_terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" '
        # Add the threads
        if timelapse_args.threads != -1:
            audio_terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        audio_terms += f'-c:a mp3 "{temp_out}"'
        runFFmpeg(audio_terms)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Created the unfaded output audio "{temp_out}" after {duration} seconds'
        )
        # Create t
        # Create the fade
        logger.info(f'Fading the output audio "{output_file}"')
        start = time.perf_counter()
        # Get durations
        fade_duration = getFadeTime(
            temp_out,
            timelapse_args.output_audio_fade_in,
            timelapse_args.output_audio_fade_out,
        )
        audio_terms = "ffmpeg "
        # Add the input file
        audio_terms += f'-i "{temp_out}" '
        # Add the threads
        if timelapse_args.threads != -1:
            audio_terms += f"-threads {timelapse_args.threads} "
        # Add the fades
        audio_terms += f'-af "'
        # Add the fade in if there is one
        if fade_duration["fade_in_l"] != 0:
            audio_terms += f'afade=t=in:st=0:d={fade_duration["fade_in_l"]},'
        # Add the fade out if there is one
        if fade_duration["fade_out_l"] != 0:
            audio_terms += f'afade=t=out:st={fade_duration["fade_out_s"]}:d={fade_duration["fade_out_l"]}"'
        # If there isn't a fade out replace the comma with a double quote
        else:
            audio_terms = audio_terms[:-1]
            audio_terms += f'"'
        # Change the audio codec (can't seem to copy it if fading)
        audio_terms += f' -c:a mp3 "{output_file}"'
        # Run ffmpeg
        runFFmpeg(audio_terms)
        # Remove the temp file if setting isn't enabled
        if not timelapse_args.keep_unfaded_audio:
            os.remove(temp_out)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully faded the output audio "{output_file}" after {duration} seconds'
        )
    # If not using a fade just output it
    else:
        # Merge the audio files
        audio_terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" '
        # Add the threads
        if timelapse_args.threads != -1:
            audio_terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        audio_terms += f'-c:a mp3 "{output_file}"'
        runFFmpeg(audio_terms)


# Function to create the combined audio and log
def logCombineAudio(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    # Create the audio for the timelapse
    logger.info(f'Creating the new audio for the timelapse at "{output_file}"')
    start = time.perf_counter()
    combineAudio(concat_file, output_file)
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
    concatFile(audio_order, audio_concat, False)
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


# Function to get the cut times
def getClipTime(
    file: pathlib.Path,
    cut_in: float,
    cut_out: float,
    cut_out_from_end: bool,
    prompted: bool,
) -> dict:
    # Get the length of the file
    duration = getLength(file)
    # If we are cutting seconds from the end
    if cut_out_from_end:
        # Get the time to cut at
        new_duration = duration - cut_out
    # If we are passing in the actual time to clip at
    else:
        new_duration = cut_out
    # Getting the new length after both buts
    new_length = new_duration - cut_in
    # Run a test if this is being called without prompt and attempt to create valid cuts,
    # if this is being ran by a prompt the prompt already wont accept the failed results
    # Checking to make sure the cuts aren't longer than the video
    if not prompted:
        # If the clip is less than 0 (not more than because I don't want it equal to 0 either) or somehow got longer there's a problem
        if not new_length > 0 or new_length > duration:
            # I'm going to choose to prioritize the cut in over the cut out
            # I'm prioritizing the cut in because in my own uses there's always a delay after starting the timelapse, but
            # many of my videos end because the camera ran out of file size per video or the camera died.
            # Check if just the cut in is valid
            if duration - cut_in > 0:
                # Check if the remaining duration is more than 1 second
                if duration - cut_in > 1:
                    # If it is we cut out everything except for 1 second
                    remaining_time = duration - cut_in - 1
                    logger.warning(
                        f'Cut at "{file}" was problematic. The remaining length will be 1 second with the cut in preserved, but the cut out was modified to leave 1 second remaining.'
                    )
                    return {
                        "cut_in": cut_in,
                        "cut_out": remaining_time,
                        "new_duration": (duration - remaining_time),
                        "output_length": 1,
                    }
                # If it's not we just return the cut in
                else:
                    logger.warning(
                        f'Cut at "{file}" was problematic. The remaining length will be {duration - cut_in} seconds with the cut in preserved, but the cut out was discarded.'
                    )
                    return {
                        "cut_in": cut_in,
                        "cut_out": 0,
                        "new_duration": duration,
                        "output_length": duration - cut_in,
                    }
            # Check if just the cut out is valid
            elif (duration - new_duration) > 0 and new_duration < duration:
                # If it's more than 1
                if (duration - new_duration) > 1:
                    # If it is we cut out everything except for 1 second
                    remaining_time = (duration - new_duration) - 1
                    logger.warning(
                        f'Cut at "{file}" was problematic. The remaining length will be 1 second with the cut out preserved, but the cut in was modified to leave 1 second remaining.'
                    )
                    return {
                        "cut_in": remaining_time,
                        "cut_out": cut_out,
                        "new_duration": new_duration,
                        "output_length": 1,
                    }
                # If it's not we just return the cut out
                else:
                    logger.warning(
                        f'Cut at "{file}" was problematic. The remaining length will be {duration - new_duration} seconds with the cut out preserved, but the cut in was discarded.'
                    )
                    return {
                        "cut_in": 0,
                        "cut_out": cut_out,
                        "new_duration": new_duration,
                        "output_length": duration - new_duration,
                    }
            # If both are invalid we ignore the clips and return a value for no clips
            else:
                return {
                    "cut_in": 0,
                    "cut_out": 0,
                    "new_duration": duration,
                    "output_length": duration,
                }
        # If clip is good
        else:
            # Get the cut times
            return {
                "cut_in": cut_in,
                "cut_out": cut_out,
                "new_duration": new_duration,
                "output_length": new_length,
            }
    # If we are prompted just return the results
    else:
        # Get the cut times
        return {
            "cut_in": cut_in,
            "cut_out": cut_out,
            "new_duration": new_duration,
            "output_length": new_length,
        }


# Function to get the fade times
def getFadeTime(
    file: pathlib.Path,
    fade_in_l: float,
    fade_out_l: float,
) -> dict:
    # Get the length of the file
    duration = getLength(file)
    # Get the fade times
    fade_out_s = duration - fade_out_l
    # Checking to make sure the fades aren't longer than the video
    # Unlike getClipTime() this will always be ran without user input
    if (fade_in_l + fade_out_l) > duration:
        logger.warning(
            f'Total fade time given for file "{file}" is longer than the file. Both fades have been made to half the file\'s duration.)'
        )
        # In the even the given fade times are larger than the duration we just fade the entire video
        duration_2 = duration / 2
        return {
            "fade_in_l": duration_2,
            "fade_out_l": duration_2,
            "fade_out_s": (
                duration - duration_2
            ),  # Just in case of rounding errors or other such silliness
        }
    else:
        return {
            "fade_in_l": fade_in_l,
            "fade_out_l": fade_out_l,
            "fade_out_s": fade_out_s,
        }


# Function to return the default dictionary (from cli arguments)
def userDefault(file_type: bool) -> List[dict]:
    if file_type == "video":
        speed_factor = timelapse_args.speed_factor
        clip_in = timelapse_args.video_clip_in
        clip_out = timelapse_args.video_clip_out
        fade_in = timelapse_args.video_fade_in
        fade_out = timelapse_args.video_fade_out
    elif file_type == "audio":
        speed_factor = timelapse_args.audio_speed_factor
        clip_in = timelapse_args.audio_clip_in
        clip_out = timelapse_args.audio_clip_out
        fade_in = timelapse_args.audio_fade_in
        fade_out = timelapse_args.audio_fade_out
    else:
        speed_factor = timelapse_args.image_length
        clip_in = timelapse_args.video_clip_in
        clip_out = timelapse_args.video_clip_out
        fade_in = timelapse_args.video_fade_in
        fade_out = timelapse_args.video_fade_out
    return [
        {
            "speed_factor": speed_factor,
            "clip_in": clip_in,
            "clip_out": clip_out,
            "clip_from_end": True,
            "fade_in": fade_in,
            "fade_out": fade_out,
        }
    ]


# Function to prompt user or input the default amount
def promptUser(file: pathlib.Path, file_type: str) -> dict:
    if timelapse_args.prompt:
        return userSettings(file, file_type)
    else:
        return userDefault(file_type)


# Function to get which files to ask the user about
def promptFiles(
    files: dict, temp_files: list, file_type: str, current_answers: dict
) -> dict:
    # For every file passed in
    for file in files:
        # If we're using settings
        if timelapse_args.use_settings:
            # If the file exists in the dictionary already and we're overriding it,
            # or if the file doesn't exist in the dictionary
            if (
                file in current_answers.keys() and timelapse_args.override_settings
            ) or file not in current_answers.keys():
                # If the file isn't an image
                if file_type != "image":
                    # Check that the file isn't already a temp file
                    if file not in temp_files:
                        current_answers[file] = promptUser(file, file_type)
                    # If they are a temp video file
                    elif file_type == "video":
                        # If we're overriding temp videos
                        if timelapse_args.override_temp_video:
                            current_answers[file] = promptUser(file, file_type)
                    # If it's audio
                    else:
                        # If we're overriding temp audio
                        if timelapse_args.override_temp_audio:
                            current_answers[file] = promptUser(file, file_type)
                # If the file type is an image
                else:
                    # Change the file name we're using to be the output of the image process
                    out_file = pathlib.Path.joinpath(
                        timelapse_args.temp_directory, f"{file.stem}.mp4"
                    )
                    # Check that the file isn't already a temp file
                    if out_file not in temp_files:
                        current_answers[file] = promptUser(file, file_type)
                    # If they are a temp video file
                    else:
                        # If we're overriding temp videos
                        if timelapse_args.override_temp_video:
                            current_answers[file] = promptUser(file, file_type)
        # If we're not using settings
        else:
            # If the file isn't an image
            if file_type != "image":
                # Check that the file isn't already a temp file
                if file not in temp_files:
                    current_answers[file] = promptUser(file, file_type)
                # If they are a temp video file
                elif file_type == "video":
                    # If we're overriding temp videos
                    if timelapse_args.override_temp_video:
                        current_answers[file] = promptUser(file, file_type)
                # If it's audio
                else:
                    # If we're overriding temp audio
                    if timelapse_args.override_temp_audio:
                        current_answers[file] = promptUser(file, file_type)
            # If the file type is an image
            else:
                # Change the file name we're using to be the output of the image process
                out_file = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}.mp4"
                )
                # Check that the file isn't already a temp file
                if out_file not in temp_files:
                    current_answers[file] = promptUser(file, file_type)
                # If they are a temp video file
                else:
                    # If we're overriding temp videos
                    if timelapse_args.override_temp_video:
                        current_answers[file] = promptUser(file, file_type)
    # Return the updating dictionary
    return current_answers


# Function to get the default order (sort the dictionaries)
def defaultOrder(file_list: dict) -> dict:
    # # Sorted Method (List)
    # # Get the unsorted list from the dict keys
    # unsorted_list = list(file_list.keys())
    # # Sorting the list by the file name (could do stem too)
    # sorted_list = sorted(unsorted_list, key=lambda x: x.name)
    # return sorted_list

    # # Sort Method (List [in place])
    # listed_file = list(file_list.keys())
    # listed_file.sort(key=lambda x: x.name)
    # return listed_file

    # Dictionary Method
    listed_file = list(file_list.keys())
    listed_file.sort(key=lambda x: x.name)
    sorted_dict = {}
    for item in listed_file:
        sorted_dict[item] = file_list[item]
    return sorted_dict


# Function to ask the user about the order
def userOrder(
    video_list: dict, audio_list: dict, user_prompt: bool
) -> Tuple[dict, dict]:
    # Variables to store the results
    video_order = {}
    audio_order = {}
    # Amount of clips
    video_len = len(video_list)
    audio_len = len(audio_list)
    # Getting the user responses
    video_options = [x for x in range(1, video_len + 1)]
    for video, source in video_list.items():
        # If we're getting responses from the user
        if user_prompt:
            # Using 1 to start instead of 0 because I think that makes more sense for non-programmer nerds
            response = getPosition(
                f'What position would you like the file "{video.name}" from "{source.name}" to be in?\nThe options are {", ".join(map(str,video_options))}, or 0 for the next position\n',
                video_options,
            )
            if response != 0:
                video_order[response] = video
                video_options.remove(response)
            else:
                video_order[video_options[0]] = video
                video_options.remove(video_options[0])
        # If we're just getting the default order
        else:
            video_order[video_options[0]] = video
            video_options.remove(video_options[0])
    # Repeated code, but it is what it is. Don't want to make another function right now.
    audio_options = [x for x in range(1, audio_len + 1)]
    for audio, source in audio_list.items():
        # If we're getting responses from the user
        if user_prompt:
            # Using 1 to start instead of 0 because I think that makes more sense for non-programmer nerds
            response = getPosition(
                f'What position would you like the file "{audio.name}" from "{audio.name}" to be in?\nThe options are {", ".join(map(str,audio_options))}, or 0 for the next position\n',
                audio_options,
            )
            if response != 0:
                audio_order[response] = audio
                audio_options.remove(response)
            else:
                audio_order[audio_options[0]] = audio
                audio_options.remove(audio_options[0])
        # If we're just getting the default order
        else:
            audio_order[audio_options[0]] = audio
            audio_options.remove(audio_options[0])
    # Sort the results (we shouldn't need to if the user didn't customize them)
    if user_prompt:
        video_order = dict(sorted(video_order.items()))
        audio_order = dict(sorted(audio_order.items()))
    # Return the results
    return video_order, audio_order


# Function to determine if we ask the user for a specific order
def promptOrder(user_answers: dict) -> Tuple[dict, dict]:
    # Variables to store them
    video_order = {}  # and converted images
    audio_order = {}
    # Get all of the files and their clips
    for file, data in user_answers.items():
        # Get the amount of clips
        for index in range(len(data)):
            # Generate paths
            if file.suffix.lower() in [".mp4", ".mkv"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                video_order[new_path] = file
            elif file.suffix.lower() in [".png", ".jpg"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}.mp4"
                )
                video_order[new_path] = file
            elif file.suffix.lower() in [".wav", ".mp3"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                audio_order[new_path] = file
    # Get the sorted orders
    video_order = defaultOrder(video_order)
    audio_order = defaultOrder(audio_order)
    # Return the values
    return (video_order, audio_order)


# Function to get a int (bool) from the user
def getIntBool(question: str) -> float:
    while True:
        try:
            response = int(input(question))
            if response in [0, 1]:
                return response
            else:
                print("That is an invalid input. Must be a 0 or 1")
        except KeyboardInterrupt:
            print("bye bye")
            sys.exit()
        except ValueError:
            print("That is an invalid input. Must be a 0 or 1")


# Function to get a int from the user
def getPosition(question: str, options: List[int]) -> int:
    while True:
        try:
            response = int(input(question))
            if response in options or response == 0:
                return response
            else:
                print(
                    f'That is an invalid input. Must be in {", ".join(map(str,options))}, or 0 for the next position'
                )
        except KeyboardInterrupt:
            print("bye bye")
            sys.exit()
        except ValueError:
            print(
                f'That is an invalid input. Must be in {", ".join(map(str,options))}, or 0 for the next position'
            )


# Function to get a float from the user
def getFloat(question: str) -> float:
    while True:
        try:
            response = float(input(question))
            # All of out responses need to be positive
            if response >= 0 or response == -1:
                return response
            else:
                print("Invalid input. Must be a positive float (decimal), 0, or -1")
        except KeyboardInterrupt:
            print("bye bye")
            sys.exit()
        except ValueError:
            print("Invalid input. Must be a positive float (decimal).")


# Function to add the audio to the timelapse
def addAudio(video_path: pathlib.Path, audio_path: pathlib.Path) -> None:
    # Output path
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
            video_audio_terms = (
                f'ffmpeg -i "{video_path}" -i "{audio_path}" -vf "{resize_vf}" '
            )
            # Add the threads
            if timelapse_args.threads != -1:
                video_audio_terms += f"-threads {timelapse_args.threads} "
            # Add the rest of the terms
            video_audio_terms += f'-map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
            # Create the timelapse
            logger.info(f'Creating the timelapse with audio at "{video_out_audio}"')
            start = time.perf_counter()
            # Run the command and wait for it to finish
            runFFmpeg(video_audio_terms)
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully created the timelapse with audio at "{video_out_audio}" after {duration} seconds'
            )
    # If the file doesn't exist (duplicate code :pained_emoji:)
    else:
        # Create the video with audio
        video_audio_terms = (
            f'ffmpeg -i "{video_path}" -i "{audio_path}" -vf "{resize_vf}" '
        )
        # Add the threads
        if timelapse_args.threads != -1:
            video_audio_terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
        video_audio_terms += f'-map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
        # Create the timelapse
        logger.info(f'Creating the timelapse with audio at "{video_out_audio}"')
        start = time.perf_counter()
        # Run the command and wait for it to finish
        runFFmpeg(video_audio_terms)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully created the timelapse with audio at "{video_out_audio}" after {duration} seconds'
        )


# Function to create the modified output
def createModifiedOutput(
    input_path: pathlib.Path, output_path: pathlib.Path, file_type: bool
) -> None:
    # Create the timelapse
    logger.info(f'Creating the modified timelapse at "{output_path}"')
    start = time.perf_counter()
    # Basic terms
    video_terms = f'ffmpeg -i "{input_path}" '
    # Add the threads
    if timelapse_args.threads != -1:
        video_terms += f"-threads {timelapse_args.threads} "
        # Add the rest of the terms
    # If we are resizing the video
    if timelapse_args.resize != 0:
        video_terms += (
            f'-vf "scale=iw*{timelapse_args.resize}:ih*{timelapse_args.resize}" '
        )
    if timelapse_args.compression_level != -1:
        video_terms += f"-crf {timelapse_args.compression_level} "
    # Check if we're applying any video fade
    if (
        timelapse_args.modified_output_video_fade_in != 0
        or timelapse_args.modified_output_video_fade_out != 0
    ):
        # Get the fades
        video_fade_duration = getFadeTime(
            input_path,
            timelapse_args.modified_output_video_fade_in,
            timelapse_args.modified_output_video_fade_out,
        )
        # Add the fades
        terms += f'-vf "'
        # Add the fade in if there is one
        if video_fade_duration["fade_in_l"] != 0:
            terms += f'fade=t=in:st=0:d={video_fade_duration["fade_in_l"]},'
        # Add the fade out if there is one
        if video_fade_duration["fade_out_l"] != 0:
            terms += f'fade=t=out:st={video_fade_duration["fade_out_s"]}:d={video_fade_duration["fade_out_l"]}" '
        # If there isn't a fade out replace the comma with a double quote
        else:
            terms = terms[:-1]
            terms += f'" '
    # Check if we're applying any audio fade (and will have audio in the modified output)
    if (
        timelapse_args.modified_output_video_fade_in != 0
        or timelapse_args.modified_output_video_fade_out != 0
    ) and (not file_type or timelapse_args.preserve_audio):
        # Get the fades
        audio_fade_duration = getFadeTime(
            input_path,
            timelapse_args.modified_output_audio_fade_in,
            timelapse_args.modified_output_audio_fade_out,
        )
        # Add the fades
        terms += f'-af "'
        # Add the fade in if there is one
        if audio_fade_duration["fade_in_l"] != 0:
            terms += f'afade=t=in:st=0:d={audio_fade_duration["fade_in_l"]},'
        # Add the fade out if there is one
        if audio_fade_duration["fade_out_l"] != 0:
            terms += f'afade=t=out:st={audio_fade_duration["fade_out_s"]}:d={audio_fade_duration["fade_out_l"]}" '
        # If there isn't a fade out replace the comma with a double quote
        else:
            terms = terms[:-1]
            terms += f'" '
    # Change the video codec
    video_terms += f"-c:v libx265 "
    # If it's a timelapse with audio, or we're preserving audio change the audio codec
    if not file_type or timelapse_args.preserve_audio:
        video_terms += f"-c:a mp3 "
    # If it's just video remove the audio
    else:
        video_terms += f"-an "
    # Add the rest of the terms
    video_terms += f'-r {timelapse_args.output_fps} "{output_path}"'
    # Run ffmpeg
    runFFmpeg(video_terms)
    # End the log
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created the modified timelapse at "{output_path}" after {duration} seconds'
    )


# Function to create the modified timelapse (resized and/or compressed)
def modifyOutput(input_path: pathlib.Path, file_type: bool) -> None:
    # Output path
    modified_video_out = pathlib.Path.joinpath(
        timelapse_args.output_directory, "timelapse_modified.mp4"
    )
    # Check if a output audio already exists
    if checkPath(modified_video_out):
        # Delete the existing output video with audio file if that setting is enabled
        if timelapse_args.override_output:
            logger.info(
                f'Deleting existing modified output timelapse "{modified_video_out}"'
            )
            os.remove(modified_video_out)
            logger.info(
                f'Deleted existing modified output timelapse "{modified_video_out}"'
            )
            # Create the timelapse
            createModifiedOutput(input_path, modified_video_out, file_type)
    # If the file doesn't exist (duplicate code :pained_emoji:)
    else:
        # Create the timelapse
        createModifiedOutput(input_path, modified_video_out, file_type)


# Function to read json of the userSetting
def loadJson(file: pathlib.Path, file_type: bool) -> dict:
    with open(file, "r") as json_file:
        data = json.load(json_file)
    # Turn the strings into paths
    new_data = convertFromJson(data, file_type)
    # Replacing the paths if the setting is enabled
    if timelapse_args.override_source_path:
        repathed_data = {}
        # Repathing for the settings file
        if file_type:
            for path, settings in new_data.items():
                # Getting the relative path by basically removing everything before the parent directory
                source_path = path.relative_to(str(path.parent.parent))
                # Getting the file type (video or audio)
                file_type = str(source_path.parent)
                # Creating the new path
                if file_type == "video":
                    new_path = pathlib.Path.joinpath(
                        timelapse_args.video_directory, path.name
                    )
                elif file_type == "audio":
                    new_path = pathlib.Path.joinpath(
                        timelapse_args.audio_directory, path.name
                    )
                else:
                    logger.warning(
                        f'The file "{path}" in the settings wasn\'t a video or audio file and has been ignored when repathing.'
                    )
                    continue
                repathed_data[new_path] = settings
        # Repathing for the order file
        else:
            for category in new_data:
                repathed_data[category] = {}
                for order, path in new_data[category].items():
                    new_path = pathlib.Path.joinpath(
                        timelapse_args.temp_directory, path.name
                    )
                    repathed_data[category][order] = new_path
            # Return the repathed data
        return repathed_data
    # If we're not replacing the paths just return the loaded data
    return new_data


# Function to transform all the strings from the settings into paths
def convertFromJson(settings: dict, file_type: bool) -> dict:
    new_dict = {}
    # Conversion for settings
    if file_type:
        for path, settings in settings.items():
            new_path = pathlib.Path(path)
            new_dict[new_path] = settings
    # Conversion for order
    else:
        for category in settings:
            new_dict[category] = {}
            for order, path in settings[category].items():
                new_path = pathlib.Path(path)
                new_dict[category][order] = new_path
    return new_dict


# Function to transform all the paths in the settings into strings
def convertToJson(settings: dict, file_type: bool) -> dict:
    new_dict = {}
    # Conversion for settings
    if file_type:
        for path, settings in settings.items():
            new_path = str(path.resolve())
            new_dict[new_path] = settings
    # Conversion for order
    else:
        for category in settings:
            new_dict[category] = {}
            for order, path in settings[category].items():
                new_path = str(path.resolve())
                new_dict[category][order] = new_path
    return new_dict


# Function to write json of the userSetting
def writeJson(file: pathlib.Path, userSettings: dict, file_type: bool) -> None:
    # Transform the paths into strings
    write_dict = convertToJson(userSettings, file_type)
    with open(file, "w+") as json_file:
        json_dump = json.dumps(write_dict, indent=4)
        json_file.write(json_dump)


# Function to get the user to enter the information about the clip and fade for each file
def userSettings(file: pathlib.Path, file_type: str) -> dict:
    print(f"The following questions are about the file {file.name}:")
    # Ask if they even want to modify this file
    wanted = getIntBool(
        "Do you want to make additional modification to this file: Yes [0] or No [1]?\n"
    )
    if wanted == 0:
        wanted = True
    elif wanted == 1:
        wanted = False
    # If they want to modify the file
    if wanted:
        # Create an item to store the response
        response = []
        while True:
            # Inform them of the option
            print("Answer the following questions  (-1 means default, 0 means disable)")
            # Get the speed factor
            while True:
                if not file_type == "image":
                    speed_factor = getFloat(
                        "How much do you want to speed up the file?\n"
                    )
                else:
                    speed_factor = getFloat(
                        "How many seconds do you want the image to last?\n"
                    )
                # Check if it's valid
                if file_type == "video":
                    if speed_factor == -1:
                        speed_factor = timelapse_args.speed_factor
                    break
                elif file_type == "audio":
                    if (
                        (speed_factor >= 0.5 and speed_factor <= 100)
                        or speed_factor == 0
                        or speed_factor == -1
                    ):
                        if speed_factor == -1:
                            speed_factor = timelapse_args.audio_speed_factor
                        break
                    else:
                        print(
                            "Speed factor for audio must be between 0.5 and 100, 0 to disable, or -1 for default"
                        )
                else:
                    # The image needs to be at least 1 frame in length
                    if (speed_factor > (1 / timelapse_args.output_fps)) or (
                        speed_factor == -1
                    ):
                        if speed_factor == -1:
                            speed_factor = timelapse_args.image_length
                        break
                    else:
                        print(
                            f"Speed factor for an image must be larger than 1 output frame length ({1/timelapse_args.output_fps} seconds at the output fps), or -1 for default"
                        )
            # Get file modifications
            while True:
                # Set bool for errors
                has_error = False
                # Get the clip in duration
                clip_in = getFloat(
                    "How many seconds do you want to clip from the start?\n"
                )
                if clip_in == -1:
                    if file_type:
                        clip_in = timelapse_args.video_clip_in
                    else:
                        clip_in = timelapse_args.audio_clip_in
                # Get the type of clip from the end
                clip_from_end = getIntBool(
                    "Do you want to clip out with the ending time (in seconds) of the clip [0] or with the seconds cut from the end [1]? (If using the default option for clip out this choice doesn't matter)\n"
                )
                if clip_from_end == 0:
                    clip_from_end = False
                elif clip_from_end == 1:
                    clip_from_end = True
                # Get the clip end duration
                if clip_from_end:
                    clip_out = getFloat(
                        "How many seconds do you wish to cut form the end?\n"
                    )
                else:
                    clip_out = getFloat(
                        "What time (in seconds) do you want to file to end?\n"
                    )
                if clip_out == -1:
                    # Going to assume if you're using the default it's form the end not an exact time
                    clip_from_end = True
                    if file_type:
                        clip_out = timelapse_args.video_clip_out
                    else:
                        clip_out = timelapse_args.audio_clip_out
                # Get the fade in duration
                fade_in = getFloat("How many seconds do you wish to fade in?\n")
                if fade_in == -1:
                    if file_type:
                        fade_in = timelapse_args.video_fade_in
                    else:
                        fade_in = timelapse_args.video_fade_out
                # Get the fade out duration
                fade_out = getFloat("How many seconds do you wish to fade out?\n")
                if fade_out == -1:
                    if file_type:
                        fade_out = timelapse_args.video_fade_out
                    else:
                        fade_out = timelapse_args.audio_fade_out
                # Validate the options given
                # Clip
                if clip_in != 0 or clip_out != 0:
                    if not file_type == "image":
                        clipped_duration = getClipTime(
                            file, clip_in, clip_out, clip_from_end, True
                        )["output_length"]
                        # Invalid length if the clipped duration is less than 0 or longer than the original
                        if not clipped_duration > 0 or clipped_duration > getLength(
                            file
                        ):
                            print("Clipped time is invalid.")
                            has_error = True
                    else:
                        # If it's an image we're doing what the function does for the video and audio here, without the validation
                        if clip_from_end:
                            # Get the time to cut at
                            new_duration = speed_factor - clip_out
                        # If we are passing in the actual time to clip at
                        else:
                            new_duration = clip_out
                        # Getting the new length after both buts
                        clipped_duration = new_duration - clip_in
                else:
                    if not file_type == "image":
                        clipped_duration = getLength(file)
                    else:
                        clipped_duration = speed_factor
                # Sped up duration
                if speed_factor != 0 and speed_factor != 1 and file_type != "image":
                    sped_duration = clipped_duration / speed_factor
                else:
                    sped_duration = clipped_duration
                # Fade
                if fade_in != 0 or fade_out != 0:
                    if (fade_in + fade_out) > sped_duration:
                        if not file_type == "image":
                            print(
                                f"Total fade time is longer than the sped up {file_type} ({round(sped_duration,2)} seconds)"
                            )
                        else:
                            print(
                                f"Total fade time is longer than the image video ({round(sped_duration,2)} seconds)"
                            )
                        has_error = True
                if not has_error:
                    break
                # If there was an error and we didn't break the loop ask again
                print(
                    f"There was an error: The following questions are about the file {file.name}:"
                )
            # If we made it this far add the current values to the response
            response.append(
                {
                    "speed_factor": speed_factor,
                    "clip_in": clip_in,
                    "clip_out": clip_out,
                    "clip_from_end": clip_from_end,
                    "fade_in": fade_in,
                    "fade_out": fade_out,
                }
            )
            # Ask if we want to make multiple clips from the video
            wanted_more = getIntBool(
                "Do you want to make another modification to this file: Yes [0] or No [1]?\n"
            )
            if wanted_more == 0:
                wanted_more = True
            elif wanted_more == 1:
                wanted_more = False
            # If we don't want to make another modification break from the while loop, if not do it again
            if not wanted_more:
                break  # Could just return in here instead, but oh well
        # Return the response
        return response
    # Return the default options (global)
    else:
        return userDefault(file_type)


# Function to create the video from the image
def ImageVideo(
    file: pathlib.Path,
    resized_image: pathlib.Path,
    image_video: pathlib.Path,
    index: int,
) -> None:
    # Creating the concat file
    concat_image = pathlib.Path.joinpath(timelapse_args.temp_directory, "image.txt")
    logger.info(f'Creating the image concat file at "{concat_image}"')
    # The speed factor for images is how many seconds you want to image to last
    output_frames = int(
        round(user_answers[file][index]["speed_factor"] * timelapse_args.output_fps, 0)
    )
    # Replace apostrophes in the file with the escape sequence ffmpeg needs
    # file_string = str(file.resolve().absolute())
    file_string = str(resized_image.resolve())
    file_string = file_string.replace("'", "'\\''")
    # New str to actually use
    temp_str = ""
    # Write a line fore each frame we want output
    for frame in range(output_frames):
        temp_str += f"file '{file_string}'\n"
    # Write the file
    with open(concat_image, "w+") as wfile:
        wfile.write(temp_str)
    logger.info(f'Created the image concat file at "{concat_image}"')
    # Creating the video from the concat file
    start = time.perf_counter()
    logger.info(f'Creating the video "{image_video}" from the image "{file}"')
    # Have to scale the image for this to work ... should probably actualyl scale all the videos to a desired resolution just in case they're not all the same resolution for some reason ... even though they should be
    # image_terms = f'ffmpeg -f concat -safe 0 -i "{concat_image}" -vf "settb=AVTB,setpts=N/{timelapse_args.output_fps}/TB,{resize_vf}" "{image_video}"'  # Maybe don't need to resize again
    image_terms = f'ffmpeg -f concat -safe 0 -i "{concat_image}" -vf "settb=AVTB,setpts=N/{timelapse_args.output_fps}/TB" "{image_video}"'
    runFFmpeg(image_terms)
    end = time.perf_counter()
    duration = end - start
    logger.info(f'Created the video "{image_video}" after {duration} seconds')
    # Deleting the concat file
    delLog(
        concat_image,
        "Deleting the temporary image concat file",
        "Deleted the temporary image concat file",
    )


# Function to check if we're making a video from an image
def logImageVideo(
    file: pathlib.Path,
    resized_image: pathlib.Path,
    image_video: pathlib.Path,
    index: int,
) -> None:
    logger.info(f'Creating the video for the image at "{file}"')
    start = time.perf_counter()
    ImageVideo(file, resized_image, image_video, index)
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created the new video for the image at "{image_video}" after {duration} seconds'
    )


# Function to create the modified video from the image video
def logModifiedImageVideo(
    file: pathlib.Path,
    image_video: pathlib.Path,
    image_video_out: pathlib.Path,
    index: int,
) -> None:
    start = time.perf_counter()
    logger.info(f'Creating new timelapse of "{image_video}" at "{image_video_out}"')
    timelapseVideo(
        image_video,
        image_video_out,
        0,
        user_answers[file][index]["clip_in"],
        user_answers[file][index]["clip_out"],
        user_answers[file][index]["clip_from_end"],
        user_answers[file][index]["fade_in"],
        user_answers[file][index]["fade_out"],
    )
    end = time.perf_counter()
    duration = end - start
    logger.info(
        f'Successfully created a timelapse of "{image_video}" after {duration} seconds'
    )


# Function to check if resolution matches
def checkResolution(file: pathlib.Path) -> bool:
    c_resolution = getResolution(file)
    if (
        c_resolution[0] != timelapse_args.width
        or c_resolution[1] != timelapse_args.height
    ):
        return False
    else:
        return True


# Function to resize the image to the output size
def resizeImage(file: pathlib.Path, resized_image: pathlib.Path) -> None:
    # Creating a scaled version of the image
    start = time.perf_counter()
    logger.info(f'Resizing the image "{file}" at "{resized_image}"')
    # Compare the resolutions
    matching_resolution = checkResolution(file)
    if not matching_resolution:
        resize_terms = f'ffmpeg -i "{file}" -vf "{resize_vf}" "{resized_image}"'
    else:
        resize_terms = f'ffmpeg -i "{file}" "{resized_image}"'
    runFFmpeg(resize_terms)
    end = time.perf_counter()
    duration = end - start
    logger.info(f'Created the resized image "{resized_image}" after {duration} seconds')


# Function to handle creating the videos from all the images
def createImage(image_files: list) -> None:
    # Turn every video into a timelapse
    for image in image_files:
        # Modifying the image
        resized_image = pathlib.Path.joinpath(
            timelapse_args.temp_directory, f"{image.stem}_r{image.suffix}"
        )
        resizeImage(image, resized_image)
        # Creating the modified versions
        image_settings = user_answers[image]
        # For every clip we're making for that file
        # for index, clips in enumerate(video_settings):
        for index in range(len(image_settings)):
            # Check if a version of it already exists
            image_video = pathlib.Path.joinpath(
                timelapse_args.temp_directory, f"{image.stem}.mp4"
            )
            # Creating the base video of the image
            if checkPath(image_video):
                # Delete the existing file if that setting is enabled
                if timelapse_args.override_temp_video:
                    delLog(
                        image_video,
                        "Deleting existing temp video created from image",
                        "Deleted existing temp video created from image",
                    )
                    # Create the new timelapse
                    logImageVideo(image, resized_image, image_video, index)
            # If the file doesn't exist just create it
            else:
                # Create the new timelapse
                logImageVideo(image, resized_image, image_video, index)

            # Creating the new output
            output = pathlib.Path.joinpath(
                timelapse_args.temp_directory, f"{image.stem}_{index}.mp4"
            )
            # Check if a timelapse already exists
            if checkPath(output):
                # Delete the existing file if that setting is enabled
                if timelapse_args.override_temp_video:
                    delLog(
                        output,
                        "Deleting existing temp video created from image",
                        "Deleted existing temp video created from image",
                    )
                    # Create the new timelapse
                    logModifiedImageVideo(image, image_video, output, index)
            # If the file doesn't exist just create it
            else:
                # Create the new timelapse
                logModifiedImageVideo(image, image_video, output, index)
        # Deleting the temporary video
        delLog(
            image_video,
            "Deleting the temporary image video",
            "Deleted the temporary image video",
        )
        # Deleting the resized image and concat file
        delLog(
            resized_image,
            "Deleting the temporary resized image",
            "Deleted the temporary resized image",
        )
        # Delete the source image file if that setting is enabled
        if timelapse_args.delete_video:
            delLog(image, "Deleting existing image", "Deleted existing image")


# Function to check if the files exist in the settings
def checkSettings(
    videos: List[pathlib.Path],
    images: List[pathlib.Path],
    audio: List[pathlib.Path],
    settings: dict,
) -> Dict[pathlib.Path, Dict[str, Union[float, int, bool]]]:
    # Combine all the source files
    source_files = videos + images + audio
    # Creating a new settings dictionary
    settings_dict = {}
    # Creating a new settings dictionary that only has values for existing source files
    for c_key, c_value in settings.items():
        if c_key in source_files:
            settings_dict[c_key] = c_value
    return settings_dict


# Function to determine if the custom order contains all the existing files (and only the existing files)
def checkOrder(custom_order: dict, user_answers: dict) -> bool:
    # Variables to store the paths
    video = {}  # and converted images
    audio = {}
    # Get all of the files and their clips from the settings
    for file, data in user_answers.items():
        # Get the amount of clips
        for index in range(len(data)):
            # Generate paths
            if file.suffix.lower() in [".mp4", ".mkv"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                video[new_path] = file
            elif file.suffix.lower() in [".png", ".jpg"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}.mp4"
                )
                video[new_path] = file
            elif file.suffix.lower() in [".wav", ".mp3"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                audio[new_path] = file
    # Checking if the custom order contains only (and all) clips from the settings
    video = set(video.keys()) == set(custom_order["video"].values())
    audio = set(audio.keys()) == set(custom_order["audio"].values())
    # Return true if both video and audio are matching
    ######## I can maybe make this so that it'll only make you renter which one is wrong
    if video and audio:
        return True
    else:
        return False


# Function to determine if the custom order contains all the existing files (and only the existing files)
def checkOrder2(custom_order: dict, user_answers: dict) -> Tuple[dict, dict]:
    # Variables to store them
    for x in custom_order:
        print(x)
    input()

    video_order = {}  # and converted images
    audio_order = {}
    # Get all of the files and their clips
    for file, data in user_answers.items():
        # Get the amount of clips
        for index in range(len(data)):
            # Generate paths
            if file.suffix.lower() in [".mp4", ".mkv"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                video_order[new_path] = file
            elif file.suffix.lower() in [".png", ".jpg"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}.mp4"
                )
                video_order[new_path] = file
            elif file.suffix.lower() in [".wav", ".mp3"]:
                new_path = pathlib.Path.joinpath(
                    timelapse_args.temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                audio_order[new_path] = file
    # Get the sorted orders
    video_order = defaultOrder(video_order)
    audio_order = defaultOrder(audio_order)
    # Return the values
    return (video_order, audio_order)


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
    action="store_true",
)
parser.add_argument(
    "-kta",
    "--keep_temp_audio",
    help="Doesn't delete the temporary audio files if passed",
    action="store_true",
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
parser.add_argument(
    "-asf",
    "--audio_speed_factor",
    help="How much do you want to speed up the audio by",
    type=float,
    default=0,
    # Default is 0 to disable it, could also be 1
)
parser.add_argument(
    "-p",
    "--prompt",
    help="Prompts the user about clipping, fading, and speed per file",
    action="store_true",
)
parser.add_argument(
    "-vci",
    "--video_clip_in",
    help="How many seconds you want to clip from the start of the video by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-vco",
    "--video_clip_out",
    help="How many seconds you want to clip from the end of the video by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-vfi",
    "--video_fade_in",
    help="How many seconds you want fade in to the video by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-vfo",
    "--video_fade_out",
    help="How many seconds you want fade out of the video by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-aci",
    "--audio_clip_in",
    help="How many seconds you want to clip from the start of the audio by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-aco",
    "--audio_clip_out",
    help="How many seconds you want to clip from the end of the audio by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-afi",
    "--audio_fade_in",
    help="How many seconds you want fade in to the audio by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-afo",
    "--audio_fade_out",
    help="How many seconds you want fade out of the audio by default",
    type=float,
    default=0,
)
parser.add_argument(
    "-ovfi",
    "--output_video_fade_in",
    help="How many seconds you want fade in to the output video",
    type=float,
    default=0,
)
parser.add_argument(
    "-ovfo",
    "--output_video_fade_out",
    help="How many seconds you want fade out of the output video",
    type=float,
    default=0,
)
parser.add_argument(
    "-oafi",
    "--output_audio_fade_in",
    help="How many seconds you want fade in to the output audio",
    type=float,
    default=0,
)
parser.add_argument(
    "-oafo",
    "--output_audio_fade_out",
    help="How many seconds you want fade out of the output audio",
    type=float,
    default=0,
)
parser.add_argument(
    "-kuv",
    "--keep_unfaded_video",
    help="Keep the unfaded output video",
    action="store_true",
)
parser.add_argument(
    "-kua",
    "--keep_unfaded_audio",
    help="Keep the unfaded output audio",
    action="store_true",
)
parser.add_argument(
    "-cl",
    "--compression_level",
    help="How compressed do you want the output",
    type=int,
    default=-1,
)
parser.add_argument(
    "-rs",
    "--resize",
    help="What scale do you want to resize the output",
    type=float,
    default=0,
)
parser.add_argument(
    "-s",
    "--settings_directory",
    help="Path to the settings directory",
    type=pathlib.Path,
)
parser.add_argument(
    "-us",
    "--use_settings",
    help="If you're using any saved settings",
    action="store_true",
)
parser.add_argument(
    "-os",
    "--override_settings",
    help="If you're going to change the settings with a prompt",
    action="store_true",
)
parser.add_argument(
    "-cs",
    "--clear_settings",
    help="Deletes the existing settings before creating new settings if passed",
    action="store_true",
)
parser.add_argument(
    "-ds",
    "--delete_settings",
    help="Deletes the settings file if passed",
    action="store_true",
)
parser.add_argument(
    "-th",
    "--threads",
    help="How many threads for ffmpeg to use",
    type=int,
    default=-1,
)
parser.add_argument(
    "-ra",
    "--randomize_audio",
    help="Randomizes the order that audio is combined (to reuse the same audio files for multiple timelapses without it getting old)",
    action="store_true",
)
parser.add_argument(
    "-rv",
    "--randomize_video",
    help="Randomizes the order that video is combined (not sure why you would ever want this, but why not)",
    action="store_true",
)
parser.add_argument(
    "-osp",
    "--override_source_path",
    help=f'Will replace the existing source paths ("video" and "audio") in the settings to the current directory paths. Useful if you\'ve moved the directories and don\'t want to update the settings file manually with prompts.',
    action="store_true",
)
parser.add_argument(
    "-pa",
    "--preserve_audio",
    help=f"Wont remove the audio tracks from the videos.",
    action="store_true",
)
parser.add_argument(
    "-movfi",
    "--modified_output_video_fade_in",
    help="How many seconds you want fade in to the modified output video",
    type=float,
    default=0,
)
parser.add_argument(
    "-movfo",
    "--modified_output_video_fade_out",
    help="How many seconds you want fade out of the modified output video",
    type=float,
    default=0,
)
parser.add_argument(
    "-moafi",
    "--modified_output_audio_fade_in",
    help="How many seconds you want fade in to the modified output audio",
    type=float,
    default=0,
)
parser.add_argument(
    "-moafo",
    "--modified_output_audio_fade_out",
    help="How many seconds you want fade out of the modified output audio",
    type=float,
    default=0,
)
parser.add_argument(
    "-il",
    "--image_length",
    help="How many seconds you want images to be by default",
    type=float,
    default=10,  # Not sure about this length, but oh well
)
parser.add_argument(
    "-dss",
    "--dont_save_settings",
    help="Doesn't save the settings if passed",
    action="store_false",
)
parser.add_argument(
    "-wi", "--width", help="The desired output width", type=int, default=1920
)
parser.add_argument(
    "-he", "--height", help="The desired output height", type=int, default=1080
)
parser.add_argument(
    "-uco",
    "--use_custom_order",
    help="If you want to use a custom order for the files to be combined",
    action="store_true",
)
parser.add_argument(
    "-oco",
    "--override_custom_order",
    help="If you're going to change the custom order with a prompt. If the files aren't the exact same you will have to override the file regardless.",
    action="store_true",
)
parser.add_argument(
    "-cco",
    "--clear_custom_order",
    help="Deletes the existing custom order before creating new settings if passed",
    action="store_true",
)
parser.add_argument(
    "-dco",
    "--delete_custom_order",
    help="Deletes the custom order file if passed",
    action="store_true",
)
parser.add_argument(
    "-dsco",
    "--dont_save_custom_order",
    help="Doesn't save the custom order if passed",
    action="store_false",
)

# Get the command line arguments
cli_args = parser.parse_args()
# print(cli_args)  # Temporary print for testing

# Call the root logger basicConfig
logging.basicConfig()
# Create root logger
logging.root.setLevel(logging.NOTSET)
# Can do this instead of the above 2
# logging.basicConfig(level=logging.NOTSET)

# Creating logger for this module
# logger = logging.getLogger(__name__)
logger = logging.getLogger("Timelapse")

## Get the command line arguments and verifying them
timelapse_args = getPaths()

# If the verbose option is passed set the logger level to info
if timelapse_args.verbose:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.WARNING)

# Variable to store the resize command that will be used many times
resize_vf = f"scale={timelapse_args.width}:{timelapse_args.height}:force_original_aspect_ratio=1,pad={timelapse_args.width}:{timelapse_args.height}:(( (ow - iw)/2 )):(( (oh - ih)/2 ))"

# If the clear options are enabled clear the directories
if timelapse_args.clear_output:
    output_files = getFiles(timelapse_args.output_directory, [".mp4", ".wav"])
    logger.info(f"Deleting all the existing outputs")
    for file in output_files:
        delLog(
            file,
            "Deleting the existing output at",
            "Deleted the existing output at",
        )
    logger.info(f"Deleted all the existing outputs")
if timelapse_args.clear_temp_audio:
    audio_files = getFiles(timelapse_args.temp_directory, [".wav", ".mp3"])
    logger.info(f"Deleting all the existing temp audio")
    for file in output_files:
        delLog(
            file,
            "Deleting the existing temp audio at",
            "Deleted the existing temp audio at",
        )
    logger.info(f"Deleted all the existing temp audio")
if timelapse_args.clear_temp_video:
    video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
    logger.info(f"Deleting all the existing temp videos")
    for file in output_files:
        delLog(
            file,
            "Deleting the existing temp videos at",
            "Deleted the existing temp videos at",
        )
    logger.info(f"Deleted all the existing temp videos")
if timelapse_args.clear_settings:
    setting_file = getFiles(timelapse_args.settings_directory, "settings.json")
    logger.info(f"Deleting the existing settings")
    delLog(
        setting_file,
        "Deleting the existing settings at",
        "Deleted the existing settings at",
    )
    logger.info(f"Deleted the existing settings")
if timelapse_args.clear_custom_order:
    custom_order_file = getFiles(timelapse_args.settings_directory, "order.json")
    logger.info(f"Deleting the existing custom order")
    delLog(
        custom_order_file,
        "Deleting the existing custom order at",
        "Deleted the existing custom order at",
    )
    logger.info(f"Deleted the existing custom order")

# Get the files
video_files = getFiles(timelapse_args.video_directory, [".mp4", ".mkv"])
audio_files = getFiles(timelapse_args.audio_directory, [".wav", ".mp3"])
image_files = getFiles(timelapse_args.video_directory, [".png", ".jpg"])

# Create a concat list of all the temp files (to ignore asking the user about them)
timelapse_video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
timelapse_audio_files = getFiles(timelapse_args.temp_directory, [".wav", ".mp3"])

# If using settings attempt ot load them
json_file = pathlib.Path.joinpath(timelapse_args.settings_directory, "settings.json")
if timelapse_args.use_settings and checkPath(json_file):
    try:
        user_answers = loadJson(json_file, True)
        logger.info(f"Loaded settings from {json_file}")
    except:
        user_answers = {}
        logger.warning(f"Settings file {json_file} is invalid and will be ignored")
else:
    user_answers = {}

# Checking and removing files from the settings that aren't in the source folders
user_answers = checkSettings(video_files, image_files, audio_files, user_answers)

# Get the user settings
user_answers = promptFiles(video_files, timelapse_video_files, "video", user_answers)
user_answers = promptFiles(audio_files, timelapse_audio_files, "audio", user_answers)
user_answers = promptFiles(image_files, timelapse_video_files, "image", user_answers)

#### Add a function to check the settings and alert the user if the audio isn't longer than the video!

# If using custom order attempt to load them (Will need to have this split the json file into video and audio) ######## NOTE
order_file = pathlib.Path.joinpath(timelapse_args.settings_directory, "order.json")
if timelapse_args.use_custom_order and checkPath(order_file):
    try:
        custom_order = loadJson(order_file, False)
        logger.info(f"Loaded the custom order from {order_file}")
    except:
        custom_order = {"video": {}, "audio": {}}
        logger.warning(f"Custom order file {order_file} is invalid and will be ignored")
else:
    custom_order = {"video": {}, "audio": {}}

# If we're using a custom order
if timelapse_args.use_custom_order:
    # If we're prompted
    if timelapse_args.prompt:
        # If we're overriding the custom order regardless ask them for their order
        if timelapse_args.override_custom_order:
            video_order, audio_order = promptOrder(user_answers)
            video_order, audio_order = userOrder(video_order, audio_order, True)
        # If we're not overriding check that the loaded order only has the paths from the settings
        elif checkOrder(custom_order, user_answers):
            # Use the loaded order
            video_order = custom_order["video"]
            audio_order = custom_order["audio"]
        # If it doesn't (or has other files) get the default and prompt the user
        else:
            video_order, audio_order = promptOrder(user_answers)
            video_order, audio_order = userOrder(video_order, audio_order, True)
    # If we aren't prompted
    else:
        # Check that the loaded order only has the paths from the settings
        if checkOrder(custom_order, user_answers):
            # Use the loaded order
            video_order = custom_order["video"]
            audio_order = custom_order["audio"]
        # If it doesn't (or has other files) get the default
        else:
            video_order, audio_order = promptOrder(user_answers)
            video_order, audio_order = userOrder(video_order, audio_order, False)
# If we're not using a custom order get the default order
else:
    video_order, audio_order = promptOrder(user_answers)
    video_order, audio_order = userOrder(video_order, audio_order, False)

# Create combined custom order for saving
custom_order = {"video": video_order, "audio": audio_order}

# Save the settings
if timelapse_args.dont_save_settings:
    writeJson(json_file, user_answers, True)
if timelapse_args.dont_save_custom_order:
    writeJson(
        order_file, custom_order, False
    )  ##### Will need to have this be a combination of the video and audio orders

# If there are videos
if len(video_files) != 0:
    # Create timelapses
    createTimelapses(video_files)

# If there is audio
if len(audio_files) != 0:
    # Create the modified audio
    createAudio(audio_files)

# If there are images in the video directory
if len(image_files) != 0:
    # Convert the images into videos
    createImage(image_files)

# Create an updated concat list of all the temp files
timelapse_video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
timelapse_audio_files = getFiles(timelapse_args.temp_directory, [".wav", ".mp3"])

# If there are temp videos
if len(timelapse_video_files) != 0:
    # Creating the concat of the timelapse videos
    createCombinedTimelapse(timelapse_video_files)

# If there is temp audio
if len(timelapse_audio_files) != 0:
    # Combine the audio files
    createCombinedAudio(timelapse_audio_files)

# Combine the audio and video
# Get the paths where the files should be
video_out = pathlib.Path.joinpath(timelapse_args.output_directory, "timelapse.mp4")
audio_out = pathlib.Path.joinpath(timelapse_args.output_directory, "audio.wav")
# Check if they exist
if checkPath(video_out) and checkPath(audio_out):
    addAudio(video_out, audio_out)

# Create the modified output if using it
if timelapse_args.resize != 0 or timelapse_args.compression_level != -1:
    # Get the path where it should be
    video_out_audio = pathlib.Path.joinpath(
        timelapse_args.output_directory, "timelapse_audio.mp4"
    )
    # If the audio timelapse exists use that
    if checkPath(video_out_audio):
        modifyOutput(video_out_audio, True)
    # If no audio timelapse exists use the main timelapse
    elif checkPath(video_out):
        modifyOutput(video_out, False)


# Deleting unwanted files/directories
# If the directory for source files should be empty
if timelapse_args.delete_video:
    delLog(
        timelapse_args.video_directory,
        "Deleting the video source directory ",
        "Deleted the video source directory ",
    )
if timelapse_args.delete_audio:
    delLog(
        timelapse_args.audio_directory,
        "Deleting the audio source directory ",
        "Deleted the audio source directory ",
    )
# Delete the settings if passed (even if we just saved them earlier :cry:)
if timelapse_args.delete_settings:
    delLog(
        json_file,
        "Deleting the settings at",
        "Deleted the settings at",
    )
# Delete the custom order if passed
if timelapse_args.delete_custom_order:
    delLog(
        order_file,
        "Deleting the custom order at",
        "Deleted the custom order at",
    )
# Delete the settings directory if both are true
if timelapse_args.delete_settings and timelapse_args.delete_custom_order:
    delLog(
        timelapse_args.settings_directory,
        "Deleting the settings directory ",
        "Deleted the settings directory ",
    )


# Deleting the temp directory if both temp audio and video have been removed
if not timelapse_args.keep_temp_video and not timelapse_args.keep_temp_audio:
    delLog(
        timelapse_args.temp_directory,
        "Deleting the temp directory ",
        "Deleted the temp directory ",
    )
# Heck why not even try to delete the output directory (it'll only delete it if empty)
if len(getFiles(timelapse_args.output_directory, [".wav", ".mp3"])) == 0:
    delLog(
        timelapse_args.output_directory,
        "Deleting the empty output directory ",
        "Deleted the empty output directory ",
    )

# Recording the ending time just for fun
total_end = time.perf_counter()
total_duration = total_end - total_start
duration_delta = datetime.timedelta(seconds=total_duration)
logger.info(
    f"Finished creating timelapse after {total_duration} seconds or {duration_delta}"
)

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
