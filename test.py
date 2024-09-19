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

    # print("-----Sorted Before----------")
    # # Dictionary Method
    # listed_file = list(file_list.keys())
    # listed_file.sort(key=lambda x: x.name)
    # sorted_dict = {}
    # for item in listed_file:
    #     sorted_dict[item] = file_list[item]
    #     print(item)

    # Separate the digits from the other characters
    stripped_files = {}
    for fil, source in file_list.items():
        # Split the string into a list of digits and others using regex
        stripped_t = re.split("([0-9]+)", str(fil.stem))
        stripped = []
        # Process the stripped list
        for x in stripped_t:
            # Remove the random empty characters the path returns
            if x != "":
                # Try to convert it to an int
                try:
                    stripped.append(int(x))
                except:
                    stripped.append(x)
        stripped_files[fil] = {"stripped": stripped, "source": source}
    # Sorting the lists of elements against each other

    print("Stripped Files\n------------------")
    print(stripped_files)
    print("Sorting\n------------------")
    ordered_files = sortDictionary(stripped_files)
    print("Sorted Files\n------------------")
    print(ordered_files)

    # return stripped_files


# NEW
def sortListItem(item_1, item_2):
    if item_1 < item_2:
        return True
    else:
        return False


def sortList():
    pass


def sortDictionary(unsorted: dict) -> dict:
    # Variable for storing the output
    sorted_files = []
    # Variable for storing the currently unsorted items using a deep copy
    # (none of that shallow shit wanted because we have mutable objects and it only copies immutable objects.
    # It is kind of like it's using pointer you'd use in other languages for mutable objects with a shallow copy)
    c_unsorted_files = copy.deepcopy(unsorted)
    # Printing?
    # Checking every value
    unsorted_len = len(unsorted) - 1
    print(unsorted_len)
    for n, c_output in enumerate(unsorted.items()):
        print(f"{n} ::: {c_output}")
        # Compare to each in the currently unsorted list
        for compare_output, compare_data in c_unsorted_files.items():
            

        # print(data["stripped"])


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
