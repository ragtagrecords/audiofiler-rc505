

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