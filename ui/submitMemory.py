from ui.elements import entry, warning, prompt, button
from ui.submitNumOfRepeats import submitNumOfRepeats
from services.tracksExist import tracksExist

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
            prompt.config(text="The song number is " + str(memory) +
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
