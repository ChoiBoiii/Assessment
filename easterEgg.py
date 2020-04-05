'''
Looking at this file will ruin your experience.
If you have not experienced it - turn back now.
'''

import webbrowser
import threading # yay for concurrency (not that it's really needed)

class Error(Exception):
    pass

class HoganError(Error):
    def __init__(self, msg):
        self.msg = msg

class IdiotError(Error):
    def __init__(self, msg):
        self.msg = msg

# Can be raised at any time
idiot = IdiotError("It says right here you're an idiot. I mean, you did break something.")

def emergencyGameCrash(): # Just in case...
    raise idiot

# Why does this exist? I started doing one thing and another thing ended up happening. Is there a more efficient implementation? 
# Probably. Am I bothered? Nope.

def threadedTimer():
    timer = threading.Timer(3, programSanitiser) # not gonna spoil it
    timer.start()

def programSanitiser():
    threadedTimer()
    print("Remember, it's important to have clean hands!")
    err = HoganError("Wash your hands!")
    webbrowser.open("https://www.woolworths.com.au/shop/productdetails/325881/palmolive-antibacterial-odour-neutralising-hand-wash-lime")
    raise err
