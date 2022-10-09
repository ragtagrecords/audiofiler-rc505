from ui.elements import prompt, button
from ui.start import start

def welcome():
    # welcome configuration
    prompt.config(text="Hello, let's merge some tracks my guy.")
    button.config(text="Get started", command=start)

    # add ui elements to the window
    prompt.pack()
    button.pack()
    return -1