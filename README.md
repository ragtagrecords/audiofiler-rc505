# audiofiler-rc505
RC-505 toolkit with Audiofiler support

**Download the latest build: [dist.zip](https://github.com/ragtagrecords/audiofiler-rc505/files/9034007/dist.zip)**

Normally when you are recording with an RC-505 and use all 5 tracks you must either record over an existing track or stop with 5.  

This process will allow you to continue recording to new tracks while saving each indivdual stem seperately for mixing and arranging later:

- Plug your RC-505 into your computer and drag the Audiofiler-RC505 executable into the WAV directory.

- Run the appplication.

- Pick and memory slot to create a master demo.

>![song-input](https://user-images.githubusercontent.com/40615096/177021610-0778e3e1-7875-468f-a835-ee9866960086.png)

- Here you are given options to customize your save.

- Submit and you're done.

The demo is then copied onto track 1 of the same memory slot and the other 4 tracks are cleared for you to continue recording.

The original stems will be saved locally in your RC-505 WAV directory with the option to additionally upload the song to 
>http://audiofiler.ragtagrecords.com

Using the Audiofiler API
>https://github.com/ragtagrecords/audiofiler-fs


To build the app in a Windows environment you can use this command:

`pyinstaller --onefile "Audiofiler RC-505.py"`
