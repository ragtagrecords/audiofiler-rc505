from ui.elements import checkUpload
from vars import memory, songNames
from ui.dropdown import combo

def updateUploadOption():
    global shouldUpload

    if checkUpload.get() == 1:
        print("Upload checked")
        shouldUpload = True

        combo.config(values=songNames)
        combo.set(str(memory))
        combo.pack(padx=20, pady=5)
        
    elif checkUpload.get() == 0:
        print("Upload unchecked")
        shouldUpload = False
        combo.forget()