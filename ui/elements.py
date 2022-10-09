import tkinter as tk
from tkinter import Frame
from ui.welcome import welcome

# establish ui container
window = tk.Tk()
window.title("Audiofiler RC-505")

# intial config of ui elements
prompt = tk.Label(
    fg="#5ae7ff",
    bg="#02111a",
    width=50,
    height=10,
    font=("monospace", 18)
)

button = tk.Button(
    # thisFrame,
    width=50,
    height=5,
    bg="black",
    fg="#5ae7ff",
    font=("monospace", 18)
)

entry = tk.Entry(
    # thisFrame,

    width=50,
    bg="white",
    fg="black",
    font=("monospace", 18)
)

warning = tk.Label(
    # thisFrame,

    text="Warning: invalid input",
    fg="yellow",
    bg="#02111a",
    font=("monospace", 18),
    width=50,
    height=5
)

checkUpload = tk.IntVar()

uploadOption = tk.Checkbutton(
    # thisFrame,

    text="Upload",
    bg="#02111a",
    fg="#5ae7ff",
    font=("monospace", 18),
    width=48,
    height=2,
    variable=checkUpload,
    onvalue=1,
    offvalue=0
)


# # container for dropdown
frame = Frame(window)
# # add dropdown menu of songs available from database
frame.pack()

welcome()

print("THE END")
window.mainloop()
