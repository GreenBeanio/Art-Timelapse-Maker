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

###
import re
import copy

cwd = pathlib.Path().resolve()
temp_directory = pathlib.Path.joinpath(cwd, "video")


# # Function to ask the user about the order
# def userOrder(
#     video_list: dict, audio_list: dict, user_prompt: bool
# ) -> Tuple[dict, dict]:
#     # Getting the user orders
#     video_order = getPositionRange(video_list, user_prompt)
#     audio_order = getPositionRange(audio_list, user_prompt)
#     # Sort the results (we shouldn't need to if the user didn't customize them)
#     if user_prompt:
#         video_order = dict(sorted(video_order.items())) ##### THESE?
#         audio_order = dict(sorted(audio_order.items())) ####
#     # Return the results
#     return video_order, audio_order


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
                    temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                video_order[new_path] = file
            elif file.suffix.lower() in [".png", ".jpg"]:
                new_path = pathlib.Path.joinpath(
                    temp_directory, f"{file.stem}_{index}.mp4"
                )
                video_order[new_path] = file
            elif file.suffix.lower() in [".wav", ".mp3"]:
                new_path = pathlib.Path.joinpath(
                    temp_directory, f"{file.stem}_{index}{file.suffix}"
                )
                audio_order[new_path] = file
    # Get the sorted orders
    video_order = defaultOrder(video_order)
    audio_order = defaultOrder(audio_order)
    # Return the values
    return (video_order, audio_order)


test_files = getFiles(temp_directory, [".mp4", ".wav"])
test_dict = {}
for n, x in enumerate(test_files):
    test_dict[x] = [n]
promptOrder(test_dict)
