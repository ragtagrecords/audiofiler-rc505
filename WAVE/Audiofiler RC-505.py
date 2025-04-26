# Audiofiler RC-505 Toolkit

# todo: break into services and components

# todo: remove extraneous imports
from genericpath import isdir
import os
import shutil
from os.path import exists
from unittest import suite
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime

##################
# user interface #
##################

projects_folder = "projects"

# container for interface
window = tk.Tk()
window.title("Audiofiler RC-505")
frame = Frame(window)

# UI elements attributes styles
greeting = tk.Label(
    text="Audiofiler RC-505",
    fg="#5ae7ff",
    bg="#02111a",
    width=50,
    height=10,
    font=("monospace", 18))

def welcome():
    greeting.config(text="Enter the song number in memory:")
    top_button.config(text="Submit", command=get_memory_id)
    # Add input field to window
    memory_id_entry.pack()
    # Assign default memory slot of 1
    memory_id_entry.insert(0, '1')

top_button = tk.Button(
    text="Get started",
    width=50,
    height=5,
    bg="black",
    fg="#5ae7ff",
    font=("monospace", 18),
    command=welcome
)

memory_id_entry = tk.Entry(
    width=50,
    bg="white",
    fg="black",
    font=("monospace", 18),
)

def get_memory_id():
    # get memory slot id from user
    memory_id = memory_id_entry.get()

    # determine if user input is an integer
    try:
        memory_id = int(memory_id)
        is_int = True
    except ValueError:
        is_int = False

    # if input is an integer set to memory_id
    # otherwise prompt user to try again
    if not is_int:
        # explicitly ask for a number between 1 and 100
        print("isnt int")
        warning.config(text="Please pick a number between 1 and 100")
        warning.pack()
        # reset state for new input
        memory_id_entry.delete(0, 'end')
        print("awaiting valid integer")

    # if memory id is within the 99 available slot on 505
    # and enough tracks exist in that slot
    if memory_id in range(1, 100) and tracksExist(memory_id):
        print("active memory_id slot: " + str(memory_id))
        # Reformat memory id to match RC505 convention
        memory_id = str(memory_id).zfill(3)

        # remove memory id input
        memory_id_entry.forget()
        # remove warning label
        warning.forget()

        # set new state
        greeting.config(
            text="The song number is " + str(memory_id)
            + "\n\nPackage tracks for upload\nor merge to record more."
        )
        top_button.config(text="Merge", command=lambda: mergeTracks(memory_id))
        bottom_button.config(text="Package", command=lambda: prompt_repeats(memory_id))
        # top_button.pack()
        bottom_button.pack()

    elif not memory_id in range(1, 100):
        # explicily ask for a number between 1 and 100
        warning.config(text="Please pick a number between 1 and 100")
        warning.pack()
        print("memory_id slot " + str(memory_id) + " does not exist")

        # reset for new input
        memory_id_entry.delete(0, 'end')
    elif not tracksExist(memory_id):
        # explicitly ask for a memory_id slot with stems
        warning.config(text="No tracks to merge in this memory_id slot")
        warning.pack()
        print("Either there is only one track or none")

        # reset for new input
        memory_id_entry.delete(0, 'end')

def prompt_repeats(memory_id):
    # set new state
    greeting.config(text="Would you like to extend the length of the demo?\nEnter the number of times the loop should repeat\n(1 is default)\n")

    # add number of repeats input
    repeat_entry.pack()

    # default of 1 repetition
    repeat_entry.insert(0, '1')

    top_button.config(text="Submit", command=lambda: get_num_repeats(memory_id))
    bottom_button.forget()

def get_num_repeats(memory_id):
    num_repeats = repeat_entry.get()

    # determine if user input is an integer
    try:
        num_repeats = int(num_repeats)
        is_int = True
    except ValueError:
        is_int = False

    if is_int and num_repeats in range(1, 20):
        # set new state
        greeting.config(text="Loops in memory slot " + str(memory_id) + "\n will be repeated " +
                        str(num_repeats) + " time(s).\n\nPrepared to package the trackouts with a demo")
        top_button.config(text="Continue?", command=lambda: packageTracks(memory_id, num_repeats))
        top_button.pack()
        bottom_button.forget()
    # if input is not an integer prompt user to try again
    if not is_int:
        # explicitly ask for a number between 1 and 100
        print("isnt int", input)
        warning.config(text="Please pick a number between 1 and 100")
        warning.pack()
        # reset state for new input
        repeat_entry.delete(0, 'end')
        print("awaiting valid integer")
    # if input is not with 20 repeats prompt user to try again
    if num_repeats not in range(1, 20):
        print(num_repeats)
        # display warning for invalid input
        warning.pack()
        print("number of repeats is invalid")

        # reset for new input
        repeat_entry.delete(0, "end")

        print("awaiting valid number of repeats")

        # clear and hide input and warning
        repeat_entry.delete(0, "end")
        repeat_entry.forget()
        warning.forget()

repeat_entry = tk.Entry(
    width=50,
    bg="white",
    fg="black",
    font=("monospace", 18)
)

warning = tk.Label(
    text="Warning: invalid input",
    fg="yellow",
    bg="#02111a",
    font=("monospace", 18),
    width=50,
    height=5
)

bottom_button = tk.Button(
    text="Package",
    width=50,
    height=5,
    bg="black",
    fg="#5ae7ff",
    font=("monospace", 18),
)

# add ui elements to the window
greeting.pack()
top_button.pack()

############
# backend
############

def get_timestamp():
    now = datetime.now()
    # To format the output, you can use strftime:
    formatted_date = now.strftime("%Y-%m-%d_%H_%M_%S")
    return formatted_date

def clear_tracks(memory_id, num_tracks):
    valid_delete = validate_saved_tracks(memory_id, num_tracks)
    
    if valid_delete:
        print("Save validated!")
        for i in range(1, 6):
            # construct file paths
            currFolderPath = memory_id + "_" + str(i)

            # if folder exists for current track
            if exists(currFolderPath):

                # determine if the folder is empty
                currFolderContents = os.listdir(currFolderPath)
                folderIsntEmpty = len(currFolderContents)

                if(folderIsntEmpty):
                        # delete file
                        os.remove(currFolderPath + "/" + currFolderContents[0])
                        print(currFolderPath + "/" +
                            currFolderContents[0] + " has been moved to " + projects_folder)
    else:
        warning.config(text="CRITICAL FAILURE:\nStop what you're doing!\ntalk to Tony")
        warning.pack()
        greeting.forget()
        top_button.forget()

def validate_saved_tracks(memory_id, num_tracks):
    new_directory_contents = os.listdir(f'{projects_folder}/{memory_id}')
    print("new\n", new_directory_contents)

    # Check number of tracks saved matches 505 contents
    length_match = len(new_directory_contents) == num_tracks
    
    # Check if name of each track saved matches 505 contents
    single_name_matches = []
    single_size_matches = []
    # For logging track sizes
    saved_track_sizes = []
    print("wav")
    for index, saved_name in enumerate(new_directory_contents):
        curr_wav_directory = f'{memory_id}_{index + 1}'
        wav_directory_contents = os.listdir(curr_wav_directory)
        print(f'track {index + 1}', wav_directory_contents)

        saved_track_size = os.path.getsize(f'{curr_wav_directory}/{wav_directory_contents[0]}')

        # Check name of first file in each WAV directory against each file name in new location
        single_name_match = wav_directory_contents[0] == saved_name
        single_name_matches.append(single_name_match)

        # Check size of saved files against each track prior to running copy command
        single_size_match = saved_track_size == os.path.getsize(f'{projects_folder}/{memory_id}/{saved_name}')
        single_size_matches.append(single_size_match)
        saved_track_sizes.append(saved_track_size)

    print("saved track sizes (mb)", saved_track_sizes)

    name_match = all(single_name_matches)
    size_match = all(single_size_matches)

    def test_pass(match):
        if match:
            # Pass in green
            return '\033[32mpass\033[0m'
        else:
            # Fail in red
            return '\033[31mfail\033[0m'
        
    print(f'\n#####\nTest\n#####\nlength: {test_pass(length_match)}\nname: {test_pass(name_match)}\nsize: {test_pass(size_match)}\n')

    if length_match and name_match and size_match:
        return True
    else:
        return False

def createPackagedTracksFolder(memory_id):
    # check if folder exists
    if not isdir(projects_folder):
        # create folder to stored stems seperately
        os.mkdir(projects_folder)
        print("New folder created: " + projects_folder)
    else:
        print(projects_folder + " already exists")

    # set path of curr stems folder
    tracks_folder = "projects/" + memory_id

    # create folder to store stems of project at given memory id
    try:
        os.mkdir(tracks_folder)
        print("New folder created: " + tracks_folder)
    except FileExistsError as err:
        print(err)
        print("retrying...")

        # Tag existing file and retry
        timestamp = get_timestamp()
        os.rename(tracks_folder, f'{tracks_folder}_{timestamp}')
        createPackagedTracksFolder(memory_id)

def export_master(memory_id, tracks, num_tracks, num_repeats, is_merge):
    # Check there is multiple loops to combine
    if num_tracks == 1:
        print("Only one track; nothing to merge")

    if num_tracks > 1:
        # figure out the longest loop
        longest_track_length = 0.0
        longest_track_index = 0
        for index, track in enumerate(tracks):
            if track.duration_seconds > longest_track_length:
                longest_track_length = track.duration_seconds
                longest_track_index = index + 1
        
        # scale tracks to make them equally long
        scaledTracks = []
        for track in tracks:
            currTrackLength = track.duration_seconds

            # what factor to multiply this track by
            curr_track_ratio = int(round(longest_track_length / currTrackLength))
            scaledTracks.append(track * curr_track_ratio)

        # store first scaled track in master
        master = scaledTracks[0]

        # overlay rest of scaled tracks to master
        for i in range(1, num_tracks):
            master = master.overlay(scaledTracks[i], position=0)

        # loop the track based on user selection
        master = master * num_repeats

        # clear all tracks
        clear_tracks(memory_id, num_tracks)

        if (is_merge):
            # export master to the track with longest loop
            print("longest track", longest_track_index)
            filePath = f'{memory_id}_{longest_track_index}/{memory_id}_{longest_track_index}.wav'
            master.export(filePath, format="wav")
        else:
            print('Attempt package export')
            timestamp = get_timestamp()
            filePath = f'{projects_folder}/{memory_id}/slot_{memory_id}_demo_{timestamp}.wav'
            master.export(filePath, format="wav")

# move files from individual folders into new stems folder
def findTracksForSong(memory_id, num_repeats, is_merge):
    # create folder for song stems
    createPackagedTracksFolder(memory_id)

    # array to store audio tracks as we find them
    tracks = []

    # determine if parent folder is empty
    currFolderContents = os.listdir('./')

    # for each track in the current song
    for i in range(1, 6):

        # construct file paths
        currFolderPath = memory_id + "_" + str(i)

        # if folder exists for current track
        if exists(currFolderPath):
            # determine if the folder is empty
            currFolderContents = os.listdir(currFolderPath)
            
            folderIsntEmpty = len(currFolderContents) > 0

            if(folderIsntEmpty):
                # determine if the folder contains a file with the expected name
                expectedFilePath = currFolderPath + "/" + currFolderPath + ".WAV"
                fileHasExpectedName = exists(expectedFilePath)

                if fileHasExpectedName:
                    # copy file to new folder
                    shutil.copy(expectedFilePath, f'{projects_folder}/{memory_id}')

                    # add track to list
                    tracks.append(AudioSegment.from_wav(expectedFilePath))

                    print("track found and stored", currFolderContents)
                    
        else:
            print("directory does not exist:", currFolderPath)

    # store count of how many tracks are found
    num_tracks = len(tracks)

    # if we found tracks for this song
    if num_tracks > 0:
        # export wav master that combines the tracks
        export_master(memory_id, tracks, num_tracks, num_repeats, is_merge)

        # Remove previous input
        memory_id_entry.delete(0, 'end')
        repeat_entry.forget()
        repeat_entry.delete(0, 'end')
        bottom_button.forget()

        if (is_merge):
            # display details of the export and asks user if they would like restart or exit
            greeting.config(
                text=f'slot #: {memory_id} | found {num_tracks} tracks\nYou may now close the program'
            )
            top_button.config(text="Pick new memory slot?", command=welcome)
        
        # display details of the export and asks user if they would like restart or exit
        greeting.config(
            text='Demo and trackouts are ready in projects folder\nYou may now close the program'
        )
        top_button.config(text="Pick new memory slot?", command=welcome)
    else:
        print("Did not found tracks")

# check if tracks exist at the given memory id
def tracksExist(memory_id):
    # Use 505 file name format
    slot_id = str(memory_id).zfill(3)

    empty_count = 0

    # for each track in the current song
    for i in range(1, 6):

        # construct track folder name
        track_folder_name = slot_id + "_" + str(i)

        # if folder for track exists
        if(exists(track_folder_name)):
            # if there is no wavs in the current folder
            if not os.listdir(track_folder_name):
                print("no stem here")
                empty_count += 1
        else:
            empty_count += 1

    if(empty_count == 5 or empty_count == 4):
        print("There are " + str(empty_count) + " empty tracks in memory_id slot " + slot_id)
        return False
    else:
        print("There are " + str(empty_count) + " empty tracks in memory_id slot " + slot_id)
        return True

def mergeTracks(memory_id):
    frame.forget()

    # attempt to move stems for this song to new folder
    findTracksForSong(memory_id, num_repeats=1, is_merge=True)

def packageTracks(memory_id, num_repeats):
    frame.forget()

    # Create demo and prepare tracks to upload as project
    findTracksForSong(memory_id, num_repeats, is_merge=False)

window.mainloop()
