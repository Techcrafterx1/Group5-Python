Code Structre 

This document outlines the structure of the codebase in main.py.

-*Imports*: All required modules, includinf tkinter, threading, time, json etc
-*Global Configurationa*: Constant; widgets, question_no, root initialization
-*Utility Functions*: 
    -`save()`: Saves new quizes and results to save files
    -`add()`: Add new results and quizes to pre-existing and loaded files
    -`load()`: Loads saved files into the app
    -`select_image()`: Select images fro device to be displayed
-*Loaded save files*: Load the pre-existing files
-*Quizes deep copy*: Create a deep copy of quizes for easier manipulation
-*Decorator functions*: 
    -`Unpack()`: Packs the widgets in the list 'widget' using the tkinter object method '.pack()'
    -`clear()`: Clears the screen of widgets and clears the widgets list in the codebase
-*Class*:
    ### Timer
    - Creates a dynamic countdown timer instance that recieves an arguement as the time and runs on a new thread and keeps track of time as the quiz progresses. Triggers submission on time depletion.
    - Methods:
        -`start()`: Starts the timer
        -`stop()`: Stops the timer
        -`elapsed()`: Returns the amount of time used
        -`get_time()`: Returns the current time spent at any point in time
-*Pages*: Each page is a function that clears up the screen configure its widgets and then packs them. Some pages contain functions within them that only applies to them. Each page contains a header, the app logo and a body called menu frame or home frame.
    ### Home page:
    - Contains 3 buttons in its home frame that lead to different pages.
    - Also contains a credit frame that holds each members name 
    ### Quiz menu page
    ### Result menu page
    ### Create menu page
    ### Quiz Page
    ### Result Page
    ### Create Page
-*Mainloop initialization*: Runs the app
