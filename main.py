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
        if not checkPath(video_source_directory):
            logger.critical('No "video" folder in directory or passed video directory')
            valid_arguments = False
    else:
        if checkPath(cli_args.video_directory):
            video_source_directory = cli_args.video_directory
        else:
            logger.critical("Invalid video source directory")
            valid_arguments = False
    # Getting the audio directory
    if cli_args.audio_directory is None:
        audio_source_directory = pathlib.Path.joinpath(cwd, "audio")
        if not checkPath(audio_source_directory):
            logger.critical('No "audio" folder in directory or passed audio directory')
            valid_arguments = False
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

    # Validating other inputs
    if cli_args.output_fps > 0:
        output_fps = cli_args.output_fps
    else:
        logger.critical("Invalid fps")
        valid_arguments = False
    if cli_args.speed_factor >= 0:
        speed_factor = cli_args.speed_factor
    else:
        logger.critical("Invalid speed factor")
        valid_arguments = False
    if (
        cli_args.audio_speed_factor >= 0.5 and cli_args.audio_speed_factor <= 100
    ) or cli_args.audio_speed_factor == 0:
        audio_speed_factor = cli_args.audio_speed_factor
    else:
        logger.critical("Invalid audio speed factor")
        valid_arguments = False
    ##########
    if cli_args.video_clip_in >= 0:
        video_clip_in = cli_args.video_clip_in
    else:
        logger.critical("Invalid video clip in")
        valid_arguments = False
    ###
    if cli_args.video_clip_out >= 0:
        video_clip_out = cli_args.video_clip_out
    else:
        logger.critical("Invalid video clip out")
        valid_arguments = False
    if cli_args.video_fade_in >= 0:
        video_fade_in = cli_args.video_fade_in
    else:
        logger.critical("Invalid video fade in")
        valid_arguments = False
    if cli_args.video_fade_out >= 0:
        video_fade_out = cli_args.video_fade_out
    else:
        logger.critical("Invalid video fade out")
        valid_arguments = False
    if cli_args.audio_clip_in >= 0:
        audio_clip_in = cli_args.audio_clip_in
    else:
        logger.critical("Invalid audio clip in")
        valid_arguments = False
    if cli_args.audio_clip_out >= 0:
        audio_clip_out = cli_args.audio_clip_out
    else:
        logger.critical("Invalid audio clip out")
        valid_arguments = False
    if cli_args.audio_fade_in >= 0:
        audio_fade_in = cli_args.audio_fade_in
    else:
        logger.critical("Invalid audio fade in")
        valid_arguments = False
    if cli_args.audio_fade_out >= 0:
        audio_fade_out = cli_args.audio_fade_out
    else:
        logger.critical("Invalid audio fade out")
        valid_arguments = False
    if cli_args.output_video_fade_in >= 0:
        output_video_fade_in = cli_args.output_video_fade_in
    else:
        logger.critical("Invalid output video fade in")
        valid_arguments = False
    if cli_args.output_video_fade_out >= 0:
        output_video_fade_out = cli_args.output_video_fade_out
    else:
        logger.critical("Invalid output video fade out")
        valid_arguments = False
    if cli_args.output_audio_fade_in >= 0:
        output_audio_fade_in = cli_args.output_audio_fade_in
    else:
        logger.critical("Invalid output audio fade in")
        valid_arguments = False
    if cli_args.output_audio_fade_out >= 0:
        output_audio_fade_out = cli_args.output_audio_fade_out
    else:
        logger.critical("Invalid output audio fade out")
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


# Function to get the framerate of the file
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
    cut_in: float,
    cut_out: float,
    cut_from_end: bool,
    fade_in: float,
    fade_out: float,
) -> None:
    final_output = pathlib.Path.joinpath(timelapse_args.temp_directory, file.name)
    # Variables for handling the current process
    current_input = file
    ## FFmpeg is a little fucky so I think I have to do these in multiple steps

    # Check if the file needs no modification
    if not (
        (cut_in != 0 or cut_out != 0)
        or (timelapse_args.speed_factor != 0 and timelapse_args.speed_factor != 1)
        or (fade_in != 0 or fade_out != 0)
    ):
        # All we need to do is change the codec and the framerate to match the rest of the videos
        terms = f'ffmpeg -i "{file}"-c:v libx265 -r {timelapse_args.output_fps} -an "{final_output}"'
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
        cut_duration = getClipTime(current_input, cut_in, cut_out, cut_from_end)
        terms = "ffmpeg "
        # Add the beginning cut
        if cut_duration["cut_in"] != 0:
            terms += f'-ss {cut_duration["cut_in"]} '
        # Add the input file
        terms += f'-i "{file}" '
        # Check other possibilities to see what output to use
        if (fade_in != 0 or fade_out != 0) or (
            timelapse_args.speed_factor != 1 and timelapse_args.speed_factor != 0
        ):
            temp_file = f"{file.stem}c{file.suffix}"
            output = pathlib.Path.joinpath(timelapse_args.temp_directory, temp_file)
            # Copy the video codec and remove audio
            terms += f"-c:v copy -an "
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
            terms += f"-c:v libx265 -r {timelapse_args.output_fps} -an "
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
    if timelapse_args.speed_factor != 0 and timelapse_args.speed_factor != 1:
        logger.info(f'Speeding up the temp timelapse of "{file}"')
        start = time.perf_counter()
        terms = "ffmpeg "
        # Add the input file and speed up factor
        terms += (
            f'-i "{current_input}" -vf "setpts={1/timelapse_args.speed_factor}*PTS" '
        )
        # Check other possibilities to see what output to use
        if fade_in != 0 or fade_out != 0:
            temp_file = f"{file.stem}s{file.suffix}"
            output = pathlib.Path.joinpath(timelapse_args.temp_directory, temp_file)
            # Remove audio (have to add the codec or it doesn't work, copying it doesn't work)
            terms += f'-c:v libx265 -an "{output}"'
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
            terms += f'-c:v libx265 -r {timelapse_args.output_fps} -an "{output}"'
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
        terms = "ffmpeg "
        # Add the input file
        terms += f'-i "{current_input}" '
        # Add the fades
        terms += f'-vf "'
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
        terms += f' -c:v libx265 -r {timelapse_args.output_fps} -an "{final_output}"'
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
def logTimelapses(video: pathlib.Path, output: pathlib.Path) -> None:
    # Create the new timelapse
    logger.info(f'Creating new timelapse of "{video}" at "{output}"')
    start = time.perf_counter()
    timelapseVideo(
        video,
        userAnswers[video]["clip_in"],
        userAnswers[video]["clip_out"],
        userAnswers[video]["clip_from_end"],
        userAnswers[video]["fade_in"],
        userAnswers[video]["fade_out"],
    )
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


# Function to modify an audio file
def timelapseAudio(
    file: pathlib.Path,
    cut_in: float,
    cut_out: float,
    cut_from_end: bool,
    fade_in: float,
    fade_out: float,
) -> None:
    final_output = pathlib.Path.joinpath(timelapse_args.temp_directory, file.name)
    # Variables for handling the current process
    current_input = file
    ## FFmpeg is a little fucky so I think I have to do these in multiple steps

    # Check if the file needs no modification
    if not (
        (cut_in != 0 or cut_out != 0)
        or (
            timelapse_args.audio_speed_factor != 0
            and timelapse_args.audio_speed_factor != 1
        )
        or (fade_in != 0 or fade_out != 0)
    ):
        # All we need to do is change the codec to match the rest of the audio
        terms = f'ffmpeg -i "{file}" -c:a mp3 "{final_output}"'
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
        cut_duration = getClipTime(current_input, cut_in, cut_out, cut_from_end)
        terms = "ffmpeg "
        # Add the beginning cut
        if cut_duration["cut_in"] != 0:
            terms += f'-ss {cut_duration["cut_in"]} '
        # Check other possibilities to see what output to use
        if (fade_in != 0 or fade_out != 0) or (
            timelapse_args.audio_speed_factor != 0
            and timelapse_args.audio_speed_factor != 1
        ):
            # Add the input file (can copy codec on the trim)
            terms += f'-i "{file}" -c:a copy '
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
            terms += f'-i "{file}" -c:a mp3 '
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
    if (
        timelapse_args.audio_speed_factor != 0
        and timelapse_args.audio_speed_factor != 1
    ):
        logger.info(f'Speeding up the temp audio of "{file}"')
        start = time.perf_counter()
        terms = "ffmpeg "
        # Add the input file and speed up factor (need to change codec)
        terms += f'-i "{current_input}" -af "atempo={timelapse_args.audio_speed_factor}" -c:a mp3 '
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
def logAudio(audio: pathlib.Path, output: pathlib.Path) -> None:
    # Create the new timelapse
    logger.info(f'Creating modified audio of "{audio}" at "{output}"')
    start = time.perf_counter()
    timelapseAudio(
        audio,
        userAnswers[audio]["clip_in"],
        userAnswers[audio]["clip_out"],
        userAnswers[audio]["clip_from_end"],
        userAnswers[audio]["fade_in"],
        userAnswers[audio]["fade_out"],
    )
    end = time.perf_counter()
    duration = end - start
    logger.info(f'Successfully modified audio of "{audio}" after {duration} seconds')


# Function to create audio (modify all the audio files)
def createAudio(audio_files: list) -> None:
    # Turn every video into a timelapse
    for audio in audio_files:
        # Check if a timelapse already exists
        output = pathlib.Path.joinpath(timelapse_args.temp_directory, audio.name)
        if checkPath(output):
            # Delete the existing file if that setting is enabled
            if timelapse_args.override_temp_audio:
                delLog(
                    output,
                    "Deleting existing temp audio",
                    "Deleted existing temp audio",
                )
                # Create the new timelapse
                logAudio(audio, output)
        # If the file doesn't exist just create it
        else:
            # Create the new timelapse
            logAudio(audio, output)
        # Delete the source video file if that setting is enabled
        if timelapse_args.delete_audio:
            delLog(
                audio, "Deleting existing source audio", "Deleted existing source audio"
            )


# Function to combine the audio
def combineAudio(concat_file: pathlib.Path, output_file: pathlib.Path) -> None:
    # Merge the audio files
    audio_terms = f'ffmpeg -f concat -safe 0 -i "{concat_file}" -c:a "{output_file}"'
    runFFmpeg(audio_terms)


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


# Function to get the cut times
def getClipTime(
    file: pathlib.Path, cut_in: float, cut_out: float, cut_out_from_end: bool
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
    # Get the fade times
    return {"cut_in": cut_in, "cut_out": new_duration, "new_duration": new_duration}


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
    return {
        "fade_in_l": fade_in_l,
        "fade_out_l": fade_out_l,
        "fade_out_s": fade_out_s,
    }


# Function to return the default dictionary (from cli arguments)
def userDefault(file_type: bool) -> dict:
    if file_type:
        speed_factor = timelapse_args.speed_factor
        clip_in = timelapse_args.video_clip_in
        clip_out = timelapse_args.video_clip_out
        fade_in = timelapse_args.video_fade_in
        fade_out = timelapse_args.video_fade_out
    else:
        speed_factor = timelapse_args.audio_speed_factor
        clip_in = timelapse_args.audio_clip_in
        clip_out = timelapse_args.audio_clip_out
        fade_in = timelapse_args.audio_fade_in
        fade_out = timelapse_args.audio_fade_out
    return {
        "speed_factor": speed_factor,
        "clip_in": clip_in,
        "clip_out": clip_out,
        "clip_from_end": True,
        "fade_in": fade_in,
        "fade_out": fade_out,
    }


# Function to prompt user or input the default amount
def promptUser(file: pathlib.Path, file_type: bool) -> dict:
    if timelapse_args.prompt:
        return userSettings(file, file_type)
    else:
        return userDefault(file_type)


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


###### NEW
# Function to get the user to enter the information about the clip and fade for each file
# Should add cli settings for this as well possibly to add a global setting instead
# Should also store it as json possibly for later use, but really there probably shouldn't be later use
def userSettings(file: pathlib.Path, file_type: bool) -> dict:
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
        # Inform them of the option
        print("Answer the following questions  (-1 means default, 0 means disable)")
        # Get the speed factor
        while True:
            speed_factor = getFloat("How much do you want to speed up the file?\n")
            # Check if it's valid
            if file_type:
                if speed_factor == -1:
                    speed_factor = timelapse_args.speed_factor
                break
            else:
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
        # Get file modifications
        while True:
            # Get the clip in duration
            clip_in = getFloat("How many seconds do you want to clip from the start?\n")
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
                clipped_duration = getClipTime(file, clip_in, clip_out, clip_from_end)[
                    "new_duration"
                ]
                if not clipped_duration > 0:
                    print("Clipped time is invalid.")
                    break
            else:
                clipped_duration = getLength(file)
            # Sped up duration
            if speed_factor != 0 and sped_duration != 1:
                sped_duration = clipped_duration / speed_factor
            else:
                sped_duration = clipped_duration
            # Fade
            if fade_in != 0 or fade_out != 0:
                if not (fade_in + fade_out) > sped_duration:
                    print(
                        f"Total fade time is longer than the sped up video ({round(sped_duration,2)} seconds)"
                    )
                    break
            # Return the use settings
            return {
                "speed_factor": speed_factor,
                "clip_in": clip_in,
                "clip_out": clip_out,
                "clip_from_end": clip_from_end,
                "fade_in": fade_in,
                "fade_out": fade_out,
            }
    # Return the default options (global)
    else:
        return userDefault(file_type)


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

############# Possible options
parser.add_argument(
    "-cl",
    "--compression_level",
    help="How compressed do you want the output",
    type=float,
    default=0,
)
parser.add_argument(
    "-rs",
    "--resize",
    help="What scale do you want to resize the output",
    type=float,
    default=0,
)
################


cli_args = parser.parse_args()
print(cli_args)  # Temporary print

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

# Get the files
video_files = getFiles(timelapse_args.video_directory, [".mp4", ".mkv"])
audio_files = getFiles(timelapse_args.audio_directory, [".wav", ".mp3"])

# Create a concat list of all the temp files (to ignore asking the user about them)
timelapse_video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
timelapse_audio_files = getFiles(timelapse_args.temp_directory, [".wav", ".mp3"])

#### Add saving and loading from json (cli argument possible) [Not sure about this honestly]
userAnswers = {}
# Get the user information about the clips and fades
for video in video_files:
    if video not in timelapse_video_files and not timelapse_args.override_temp_video:
        userAnswers[video] = promptUser(video, True)
for audio in audio_files:
    if audio not in timelapse_video_files and not timelapse_args.override_temp_audio:
        userAnswers[audio] = promptUser(audio, False)

# Check if there are videos in the video directory (((( DO I REALLY CARE? I could still run the audio and video Separate))))
if len(video_files) == 0:
    logger.critical("There are no videos in the video file")
    sys.exit()

# If there are videos
if len(video_files) == 0:
    # Create timelapses
    createTimelapses(video_files)
    # Creating the concat of the timelapse videos
    createCombinedTimelapse(timelapse_video_files)

# If there is audio
if len(audio_files) != 0:
    # Create the modified audio
    createAudio(audio_files)
    # Combine the audio files
    createCombinedAudio(timelapse_audio_files)

# Create an updated concat list of all the temp files
timelapse_video_files = getFiles(timelapse_args.temp_directory, [".mp4", ".mkv"])
timelapse_audio_files = getFiles(timelapse_args.temp_directory, [".wav", ".mp3"])

# Combine the audio and video
# Get the paths where the files should be
video_out = pathlib.Path.joinpath(timelapse_args.output_directory, "timelapse.mp4")
audio_out = pathlib.Path.joinpath(timelapse_args.output_directory, "audio.wav")
# Check if they exist
if checkPath(video_out) and checkPath(audio_out):
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
            vide_audio_terms = f'ffmpeg -i "{video_out}" -i "{audio_out}" -map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
            # Create the timelapse
            logger.info(f'Creating the timelapse with audio at "{video_out_audio}"')
            start = time.perf_counter()
            # Run the command and wait for it to finish
            runFFmpeg(vide_audio_terms)
            end = time.perf_counter()
            duration = end - start
            logger.info(
                f'Successfully created the timelapse with audio at "{video_out_audio}" after {duration} seconds'
            )
    # If the file doesn't exist (duplicate code :pained_emoji:)
    else:
        # Create the video with audio
        vide_audio_terms = f'ffmpeg -i "{video_out}" -i "{audio_out}" -map 0:v:0 -map 1:a:0 -shortest "{video_out_audio}"'
        # Create the timelapse
        logger.info(f'Creating the timelapse with audio at "{video_out_audio}"')
        start = time.perf_counter()
        # Run the command and wait for it to finish
        runFFmpeg(vide_audio_terms)
        end = time.perf_counter()
        duration = end - start
        logger.info(
            f'Successfully created the timelapse with audio at "{video_out_audio}" after {duration} seconds'
        )

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
