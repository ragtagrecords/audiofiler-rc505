# Audiofiler RC-505 Toolkit

# todo: break into services and components
# type things

# todo: remove extraneous imports
from genericpath import isdir
from lib2to3.pgen2.token import GREATER
import os
import shutil
from os.path import exists
from unittest import suite
from pydub import AudioSegment
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import json

#################
# user interface
#################

window = tk.Tk()
window.title("Audiofiler RC-505")


def welcome():
    greeting.config(text="Enter the song number in memory:")
    button.config(text="Submit", command=submitMemoryID)
    entry.pack()


def submitMemoryID():
    # get name of folder from user
    global memory

    input = entry.get()

    # determine if user input is an integer
    isInt = True
    try:
        int(input)
    except ValueError:
        isInt = False

    # if input is an integer set to memory
    # otherwise prompt user to try again
    if isInt:
        memory = int(input)
    else:
        # explicitly ask for a number between 1 and 100
        print("isnt int")
        warning.config(text="Please pick a number between 1 and 100")
        warning.pack()
        # reset state for new input
        entry.delete(0, 'end')
        print("awaiting valid integer")

    # determine if memory is defined
    memoryExists = True
    try:
        print("looking for memory slot " + str(memory))
    except NameError:
        print("memory slot is not defined")
        memoryExists = False

    inRange = True
    if memory not in range(1, 101):
        inRange = False
        # explicily ask for a number between 1 and 100
        warning.config(text="Please pick a number between 1 and 100")
        warning.pack()
        print("memory slot " + str(memory) + " does not exist")

        # reset for new input
        entry.delete(0, 'end')

    # if memory slot number is valid
    if memoryExists and isInt and inRange:
        print("active memory slot: " + str(memory))

        # if enough tracks exist to upload
        if tracksExist():
            # set new state
            greeting.config(text="The song number is " + str(memory) +
                            "\n Would you like to extend the length of the masters? \nEnter the number of times the loop should repeat\n(1 is default)\n")
            button.config(text="Submit", command=submitNumOfRepeats)

            # set input to default: 1
            entry.delete(0, "end")
            entry.insert(0, "1")

            # remove warning label
            warning.forget()

        else:
            # explicitly ask for a memory slot with stems
            warning.config(text="No tracks to merge in this memory slot")
            warning.pack()
            print("Either there is only one track or none")

            # todo: if there is only one track,
            # give option to upload this one without merging

            # reset for new input
            entry.delete(0, 'end')

    else:
        print("awaiting valid memory slot")

def submitNumOfRepeats():
    global numOfRepeats

    # todo: handle non numbers
    input = entry.get()

    numOfRepeats = int(entry.get())

    if numOfRepeats not in range(1, 101):
        # display warning for invalid input
        warning.pack()
        print("number of repeats is invalid")

        # reset for new input
        entry.delete(0, "end")
    else:
        print("Success: " + str(numOfRepeats) + " repeats")
        # set new state
        greeting.config(text="The song number is " + str(memory) + "\nand it will be repeated " +
                        str(numOfRepeats) + " times.\n\nAll tracks will be merged onto track 1")
        button.config(text="Merge", command=mergeTracks)

        # clear and hide input and warning
        entry.delete(0, "end")
        entry.forget()
        warning.forget()

        # add checkbox to determine if user wants to upload
        uploadOption.pack()

    print("awaiting valid number of repeats")


checkUpload = tk.IntVar()
checkSong = tk.IntVar()


def updateUploadOption():
    global shouldUpload

    if checkUpload.get() == 1:
        print("Upload checked")
        shouldUpload = True

        # add dropdown menu of songs available from database
        frame.pack()
        Combo.set(str(memory))
        Combo.pack(padx=20, pady=5)
        
    elif checkUpload.get() == 0:
        print("Upload unchecked")
        shouldUpload = False
        frame.forget()
        Combo.forget()

# UI elements attributes styles
greeting = tk.Label(
    text="Hello, let's merge some tracks my guy.",
    fg="#5ae7ff",
    bg="#02111a",
    width=50,
    height=10,
    font=("monospace", 18))

entry = tk.Entry(
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

uploadOption = tk.Checkbutton(
    text="Upload",
    bg="#02111a",
    fg="#5ae7ff",
    font=("monospace", 18),
    width=48,
    height=2,
    variable=checkUpload,
    onvalue=1,
    offvalue=0,
    command=updateUploadOption
)

button = tk.Button(
    text="Get started",
    width=50,
    height=5,
    bg="black",
    fg="#5ae7ff",
    font=("monospace", 18),
    command=welcome
)

# todo: move this request and add some kind of loading screen
if (requests.get('http://api.ragtagrecords.com/public/songs')):
    songsDatabase = (requests.get(
    'http://api.ragtagrecords.com/public/songs')).json()
    print(songsDatabase)
else: songsDatabase = []

# global vars
mode = "0"
stemsFolderPath = ""
numOfRepeats = 1
shouldUpload = False
memory = -1

# songs available to select
songs = []
songNames = []

# the result is a Python dictionary:
for song in songsDatabase:
    songObject = {"name": None, "id": None}
    songObject["name"] = song["name"]
    songObject["id"] = song["id"]
    songs.append(songObject)

for song in songs:
    songNames.append(song["name"])

# container for dropdown
frame = Frame(window)

# configure dropdown menu
Combo = ttk.Combobox(frame, values=songNames)

# add ui elements to the window
greeting.pack()
button.pack()

# name of folder for stems of a merged track
d_stems = "unmerged-stems"


############
# backend
############

def createFolderForSongStems(songNumber):
    # set path of curr stems folder
    global stemsFolderPath
    stemsFolderPath = d_stems + "/" + str(songNumber).zfill(3)

    if not isdir(stemsFolderPath):
        # create folder to stored stems of this song
        os.mkdir(stemsFolderPath)
        print("New folder created: " + stemsFolderPath)
    else:
        print(stemsFolderPath + " already exists")


def exportMaster(songNumber, tracks, numOfTracks):

    mergedTrack = str(songNumber).zfill(3) + "_1/" + \
        str(songNumber).zfill(3) + "_"

    if numOfTracks == 1:
        print("Only one track; nothing to merge")

    if numOfTracks > 1:

        # figure out the longest loop
        longestTrackLength = 0.0
        for track in tracks:
            if track.duration_seconds > longestTrackLength:
                longestTrackLength = track.duration_seconds

        # scale tracks to make them equally long
        scaledTracks = []
        for track in tracks:
            currTrackLength = track.duration_seconds

            # what factor to multiply this track by
            currTrackRatio = int(round(longestTrackLength / currTrackLength))
            scaledTracks.append(track * currTrackRatio)

        # store first scaled track in master
        master = scaledTracks[0]

        # overlay rest of scaled tracks to master
        for i in range(1, numOfTracks):
            master = master.overlay(scaledTracks[i], position=0)

        # loop the track based on user selection
        master = master * numOfRepeats

        # clear all tracks
        for i in range(1, 6):

            # construct file paths
            currFolderPath = str(songNumber).zfill(3) + "_" + str(i)

            # if folder exists for current track
            if exists(currFolderPath):

                # determine if the folder is empty
                currFolderContents = os.listdir(currFolderPath)
                folderIsntEmpty = len(currFolderContents)

                if(folderIsntEmpty):
                    os.remove(currFolderPath + "/" + currFolderContents[0])
                    print(currFolderPath + "/" +
                          currFolderContents[0] + " has been moved to " + d_stems)

        # export master
        filePath = mergedTrack + "1.wav"
        master.export(filePath, format="wav")

        # check if user selected to upload song to web
        if shouldUpload:

            # define api endpoints
            wavURL = "http://files.ragtagrecords.com/songs/"
            zipURL = "http://files.ragtagrecords.com/zips/"
            songURL = "http://api.ragtagrecords.com/public/songs"

            fileName = filePath.split("/").pop()
            
            if songSelectedID == -1:
                print("User chose to upload new song")

                # zip up the stems folder
                shutil.make_archive(stemsFolderPath, 'zip', stemsFolderPath)
                print("song zip file name: " + str(songNumber).zfill(3) + ".zip")

                songName = "my505_" + songSelected

                song = {
                    "song": {
                        "name": songName,
                        "path": wavURL + fileName,
                        # todo: make playlist select menu
                        "playlistIDs": [123],
                        "zipPath": zipURL + str(songNumber).zfill(3) + ".zip",
                    }
                }

                songFileObject = {
                    "file": open(filePath, "rb")
                }

                zipFileObjext = {
                    "file": open(stemsFolderPath + ".zip", "rb")
                }

                # upload new song
                postSong = requests.post(songURL, json=song)
                postFile = requests.post(wavURL, files=songFileObject)
                # and upload zipped stems folder
                postZip = requests.post(zipURL, files=zipFileObjext)

                print(postSong.text)
                print(postFile.text)
                print(postZip.text)

            # check if user selected a song that already exists on the database
            if songSelectedID:
                print("User chose song already on the database")
                print("parentID: " + str(songSelectedID))

                shutil.make_archive(stemsFolderPath, 'zip', stemsFolderPath)
                print("song zip file name: " + str(songNumber).zfill(3) + ".zip")

                songName = "my505_" + songSelected

                song = {
                    "song": {
                        "name": songName,
                        "path": wavURL + fileName,
                        "zipPath": zipURL + str(songNumber).zfill(3) + ".zip",
                        "parentID": songSelectedID
                    }
                }

                songFileObject = {
                    "file": open(filePath, "rb")
                }

                zipFileObjext = {
                    "file": open(stemsFolderPath + ".zip", "rb")
                }

                # upload new song
                postSong = requests.post(songURL, json=song)
                postFile = requests.post(wavURL, files=songFileObject)
                # and upload zipped stems folder
                postZip = requests.post(zipURL, files=zipFileObjext)

                print(postSong.text)
                print(postFile.text)
                print(postZip.text)

        else:
            print("User chose not to upload song")


# move files from individual folders into new stems folder
def findTracksForSong(songNumber):

    # create folder for song stems
    createFolderForSongStems(songNumber)

    # array to store audio tracks as we find them
    tracks = []

    # for each track in the current song
    for i in range(1, 6):

        # construct file paths
        currFolderPath = str(songNumber).zfill(3) + "_" + str(i)

        # if folder exists for current track
        if exists(currFolderPath):

            # determine if the folder is empty
            currFolderContents = os.listdir(currFolderPath)
            folderIsntEmpty = len(currFolderContents)

            if(folderIsntEmpty):

                # mode 0 - only moves files that have default names
                if mode == '0':

                    # determine if the folder contains a file with the expected name
                    expectedFilePath = currFolderPath + "/" + currFolderPath + ".WAV"
                    fileHasExpectedName = exists(expectedFilePath)

                    if fileHasExpectedName:

                        # copy file to new folder
                        shutil.copy(expectedFilePath, stemsFolderPath)

                        # add track to our list
                        tracks.append(AudioSegment.from_wav(expectedFilePath))

                # mode 1 - moves files with custom names as well
                elif mode == '1':

                    actualFilePath = currFolderPath + \
                        "/" + currFolderContents[0]

                    # copy file to new folder
                    shutil.copy(actualFilePath, stemsFolderPath)

                    # add track to our list
                    tracks.append(AudioSegment.from_wav(actualFilePath))

    numOfTracks = len(tracks)

    # if we found tracks for this song
    if numOfTracks:
        # export wav master that combines the tracks
        exportMaster(songNumber, tracks, numOfTracks)

        # display details of the export and asks user if they would like restart or exit
        greeting.config(text="song #: " + str(songNumber) +
                    " | found " + str(numOfTracks) + " tracks\nYou may now close the program")
        button.config(text="Continue?", command=welcome)

        return 1

    else:
        return 0


def tracksExist():
    emptyCount = 0

    # for each track in the current song
    for i in range(1, 6):

        # construct track folder name
        folderName = str(memory).zfill(3) + "_" + str(i)

        # if folder for track exists
        if(exists(folderName)):

            # if there are files in the current folder
            if not os.listdir(folderName):
                print("no stem here")
                emptyCount += 1

    if(emptyCount == 5):
        print("There are " + str(emptyCount) + " empty tracks in memory slot " + str(memory))
        return False
    elif(emptyCount == 4):
        print("There are " + str(emptyCount) + " empty tracks in memory slot " + str(memory))
        return False
    else:
        print("There are " + str(emptyCount) + " empty tracks in memory slot " + str(memory))
        return True

def getID(name):
    for song in songs:
        if song["name"] == name:
            return song["id"]

    print("no song id found with that name")
    return -1


def mergeTracks():
    # remove selection ui
    checkUpload.set(0)
    uploadOption.forget()
    frame.forget()
    Combo.forget()

    # store song selection
    global songSelected
    songSelected = (Combo.get())
    global songSelectedID
    songSelectedID = getID(songSelected)
    print("song selected: " + songSelected)
    print("id: " + str(songSelectedID))

    # check if folder exists
    if not isdir(d_stems):
        # create folder to stored stems seperately
        os.mkdir(d_stems)
        print("New folder created: " + d_stems)
    else:
        print(d_stems + " already exists")

    # let user choose config
    global mode
    # mode = input("Please choose desired mode:\n0: Only move file names that match the default RC-505 naming style\n1: Move all files no matter what their name is\n")

    # attempt to move stems for this song to new folder
    findTracksForSong(memory)
    print("after findTracksForSong()")


print("THE END")
window.mainloop()
