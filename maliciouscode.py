'''
Looking at this file will ruin your experience.
If you have not experienced it - turn back now.
'''

import webbrowser
import threading # yay for concurrency

class Error(Exception):
    pass

class ThillError(Error):
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
    timer = threading.Timer(3, notSuspiciousFunction) # not gonna spoil it
    timer.start()

def notSuspiciousFunction():
    threadedTimer()
    print("I\u0332 A\u0332M\u0332 T\u0332H\u0332E\u0332 F\u0332I\u0332N\u0332A\u0332L\u0332 B\u0332O\u0332S\u0332S\u0332")
    err = ThillError("Drats.")
    webbrowser.open("https://asset-cdn.schoology.com/system/files/imagecache/profile_reg/pictures/picture-8a57c05f0324e9001e73af6584af2c0d_58c79ad9cc67b.jpg?1489476313")
    raise err
