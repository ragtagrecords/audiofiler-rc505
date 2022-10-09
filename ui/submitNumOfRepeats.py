from ui.elements import entry, warning, prompt, button, uploadOption
from ui.updateUploadOption import updateUploadOption

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
        prompt.config(text="The song number is " + str(memory) + "\nand it will be repeated " +
                        str(numOfRepeats) + " times.\n\nAll tracks will be merged onto track 1")
        button.config(text="Merge", command=mergeTracks)

        # clear and hide input and warning
        entry.delete(0, "end")
        entry.forget()
        warning.forget()

        #configure checkbox actions
        uploadOption.config(command=updateUploadOption)

        # add checkbox to determine if user wants to upload
        uploadOption.pack()

    print("awaiting valid number of repeats")