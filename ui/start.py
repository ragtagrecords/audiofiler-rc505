from ui.elements import prompt, button, entry
# from ui.submitMemory import submitMemoryID

# prompt user for a location in memory
def start():
    prompt.config(text="Enter the song number in memory:")
    # button.config(text="Submit", command=submitMemoryID)
    entry.pack()