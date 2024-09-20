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

    # # Dictionary Method
    # listed_file = list(file_list.keys())
    # listed_file.sort(key=lambda x: x.name)
    # sorted_dict = {}
    # for item in listed_file:
    #     sorted_dict[item] = file_list[item]
    # return sorted_dict

    # Creating a more complicated sorting algorithm because of strings/paths containing numbers
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
    ordered_files = sortDictionary(stripped_files)
    return ordered_files


# NEW
# Function to compare two items against each other
def sortListItem(unsorted, sorted) -> int:
    # Check if both are ints and floats or both are strings
    if (isinstance(unsorted, (int, float)) and isinstance(sorted, (int, float))) or (
        isinstance(unsorted, str) and isinstance(sorted, str)
    ):
        if unsorted < sorted:
            return 0  # Return zero because it's larger
        elif unsorted == sorted:
            return 2  # Return 2 if they are equal and the next item should be compared
        else:
            return 1  # Return 1 if unsorted is larger
    # If unsorted is a int or float, but sorted is a str
    elif isinstance(unsorted, (int, float)) and isinstance(sorted, str):
        return 0  # Return 0 because numbers take priority over letters
    # If sorted is a int or float, but unsorted is a str
    elif isinstance(unsorted, str) and isinstance(sorted, (int, float)):
        return 1  # Return 1 because letters are always less than numbers


# Function to compare two lists against each other
def sortList(unsorted, sorted):
    # Get the length of both
    len_u = len(unsorted)
    len_s = len(sorted)
    # For the possible comparisons
    for index in range(min(len_u, len_s)):
        # Get values from both
        u_item = unsorted[index]
        s_item = sorted[index]
        # If the unsorted item is found to be smaller than the sorted item return true
        result = sortListItem(u_item, s_item)
        # Wanted to use the match for a switch statement, but I didn't have python 3.10+. Old version of ubuntu only had 3.8 :(
        # match result:
        #     case 0:
        #         return True
        #     case 1:
        #         return False
        if result == 0:
            return True
        elif result == 1:
            return False
        # If not we keep the loop going (result of 2)
    # If nothing was found to be smaller then return False
    return False


# Function to sort the dictionaries by their output name
def sortDictionary(unsorted: dict) -> dict:
    # Variable for storing the output
    sorted_files = []
    for n, c_output in enumerate(unsorted):
        # If it's the first entry
        if n == 0:
            sorted_files.append(unsorted[c_output])
            continue  # Skip the rest of the loop
        # Get the length of the current sorted file
        sorted_files_len = len(sorted_files)
        # Compare to each in the currently unsorted list
        for ni, sorted in enumerate(sorted_files):
            # If the unsorted item is smaller than the stored item insert it before it
            if sortList(unsorted[c_output]["stripped"], sorted["stripped"]):
                sorted_files.insert(ni, unsorted[c_output])
                break
            # If we are at the last index in the list
            if ni + 1 == sorted_files_len:
                sorted_files.append(unsorted[c_output])
                break  # Shouldn't need to break because it's the end, but just to be safe why not
            # If we're not keep going and check against the next sorted file
    # Transform the sorted array/list into a dictionary
    output_dict = {}
    for sort in sorted_files:
        for output, data in unsorted.items():
            # Find the matching entry from the sorted file
            if sort["source"] == data["source"]:
                output_dict[output] = data["source"]
    return output_dict


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
