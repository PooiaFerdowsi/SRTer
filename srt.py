"""
All rights are reserved for the Author.
Author: Pooia Ferdowsi <pooia.ferdowsi.is.developer@gmail.com>
You can find LICENSE in the README.md

Ensure that you always have one and only one blankline between frames
Ensure that the first line of the file is frame number
Ensure that last frame has at least two blanklines after its caption

NOTE: datetime.time.microsecond stands for millisecond
"""
from datetime import time, timedelta
import re

FROM = "D:/srt.srt" # the file to read the subtitle from
OFFSET = 0000 # time to add to timecode in miliseconds
TO = "D:" # the file to write the subtitle to

############### UTILITY ################
def read_file_splitted(path):
    """Read the file in the specified 'path' and return it splitted
    Open and read the file specifed in 'path' with given 'encoding'
    and make a list of the text which each element represents a 'line'
    in the file. (readline() method doesn't work, so it's a substitute)
    """
    return open(path, encoding='utf-8-sig').read().splitlines()

def parse_timecode(timecode):
    "return datetime.time from ' 00:00:00,000 ' pattern/format"
    hour, minute, rest = timecode.split(':')
    second, milli_sec = rest.split(',')
    # use a map, convert it to a list
    return time(
        int(hour),      int(minute),
        int(second), int(milli_sec)
        )

def isBlank(line) -> bool:
    return line.isspace() or not bool(line)

# CUSTOMIZABLE: customize 'getInfo' func as you wish
def getInfo():
    """Read and assign the desired data
    The function assign the value acquired by the implemented
    method in this function to FROM, TO, and OFFSET variables
    """
    # TODO: check answer more than now
    global FROM, TO, OFFSET
    FROM = input("File to read the data from: ")
    TO = input("File to write the data to: ")
    OFFSET =  int(input("Time to delay the captions (millisecs): "))


# CUSTOMIZABLE: customize 'do' func as you wish
def do(fr):
    "This function tells the program to do what"
    global OFFSET
    fr.setTimecodes\
                (time_sum(fr.start, OFFSET), time_sum(fr.end, OFFSET),)
    return fr.__str__()


def file2write(filename: str):
    """Create and return the file 'filename'
    Create if doesn't exist and open (in append mode)
    if exists the file 'filename' and return it
    """
    try:
        f = open(filename, 'x', encoding='utf-8-sig')
    except FileExistsError:
        f = open(filename, 'a', encoding='utf-8-sig')
    finally:
        return f

def time2msec(hour, minute, second, millisec):
    "converts (h, m, s, ms) to milliseconds"
    # millisec acts as millisecond
    return millisec + ((hour * 60 + minute) * 60 + second) * 1000
def msec2time(millisecond):
    "converts millisecond to (h, m, s, ms)"
    # how many milliseconds are there in an hour
    msec_in_hour = 3600000 # 3,600,1000 = 60^2 * 1000
    msec_in_min = 60000 # 60,000 = 60 * 1000
    msec_in_sec = 1000 # 1,000 = 1 * 1000
    hour = millisecond // msec_in_hour
    minute = (millisecond % msec_in_hour) // msec_in_min
    second = (millisecond % msec_in_min) // msec_in_sec
    msec = (millisecond % msec_in_sec)
    return hour, minute, second, msec
    

def time_sum(tm: time, offset):
    """Add offset (in milliseconds) to tm (datetime.time object)
    """
    # What about if I convert all of them to millisecond and then
    # calculate the sum and move it back to the actuall format
    if not isinstance(tm, time):
        raise Exception("datetime.time object expected")

    result = time2msec(tm.hour, tm.minute
    , tm.second, tm.microsecond) + offset
    result = 0 if result < 0 else result
    return time(*msec2time(result))

class Frame:
    """This class represents a frame in SRT
    The purposes of creation of the 'Frame' class
    is to be able to save frames in a list, which
    may not be possible because of the dense information
    a frame represent.
    """
    number = None # Frame number in the SRT file
    timecodes = None # Time to (start, end) the caption
    start, end = None, None
    caption = None
    
    def __init__(self, number: int, timecodes: tuple, caption: str):
        if number > 0:
            raise Exception\
            ("Frame number cannot be negative or zero")
        self.number = number
        self.start, self.end = timecodes
        self.setTimecodes(self.start, self.end)
        if type(caption) != str:
            raise Exception("Caption must be string")
        self.caption = caption

    def __str__(self):
        "Renders the frame as if it was in a SRT file"
        return \
        f"{self.number}\n"\
        f"{self.start.hour}:{self.start.minute}:"\
        f"{self.start.second},{self.start.microsecond}"\
        f" --> {self.end.hour}:{self.end.minute}:"\
        f"{self.end.second},{self.end.microsecond}"\
        f"\n{self.caption}\n\t\n"

    def setTimecodes(self, start, end):
        if isinstance(start, time) and isinstance(end, time):
            self.timecodes = (start, end)
            self.start, self.end = self.timecodes
        else:
            raise Exception("Timecodes must be datetime.time objects")



### functions to extract desired data from the argument $line ###
def frame_number(line: str, *):
    """Try to extract frame number from the given line
    To do it, this function tries to convert the 'line'
    parameter to a positive integer.
    "23" --> 23 --> # it's frame number
    """
    frame = int(line)
    if frame < 0:
        raise Exception("Frame number can't be zero or negative")
    return frame

def frame_timecode(line: str):
    """Read $line and return timecodes (in datetime.time)
    It first check if the line is within desired patterns
    If so, split $start & $end and passes it to
    parse_timecode() so it returns datetime.time objects
    """
    timecode_regex = ' *[0-9]+:[0-6]?[0-9]:[0-6]?[0-9],[0-9]{1,3} \
--> [0-9]+:[0-6]?[0-9]:[0-6]?[0-9],[0-9]{1,3}'
    if len(re.findall(re.compile(timecode_regex), line)) == 1:
        timecodes = line.split('-->')
        return (
            parse_timecode(timecodes[0]), # start
            parse_timecode(timecodes[1])) # end
    else:
        raise Exception("Two timecodes in a single frame/No timetimecodes")

def frame_caption(line: str, *, blank=False):
    """Read the $line and return it as caption if it's no empty
    If so, it refer to the $blank parameter and returns $blank
    This help to know can the line be blank (end of frame) or
    it's a bug.
    Remember: >>> 'str' == True -- False
    """
    if isBlank(line):
        return blank # blankline found instead of caption
    else:
        return line


# get FROM, TO, OFFSET
getInfo()

# $frame saves each frame as a dictionary til it's valued newly
frame = {} #{'number': int, 'timecodes': (,), 'caption': ''}

"""
Variable 'STATE' contain the current (previous) state of the line.
Variable 'EXPECTED' contain the state which is expected to be on
the line at the point. it must be the current state of the line.

Integer variable start with 'STATE_' are used to define line states.
"""

STATE_FRAME = 0 # it's frame number
STATE_TIME = 1 # it's hh:mm:ss,ms --> hh:mm:ss,ms
STATE_CAPTION = 2 # it's caption
STATE_BLANK = 3 # it's blank line

STATE = STATE_FRAME # default status
EXPECTED = STATE_FRAME

SUBTITLE = file2write(TO)


# Explore the file and append <class 'Frame'> objects to
# list $frames to represent the hole subtitle (SRT) file.
for line in read_file_splitted(FROM):
    if isBlank(line):
        if STATE == STATE_BLANK:
            break # tow contiguous blanlines mean EOF

    # Find state of the line and do appropriate actions
    if EXPECTED == STATE_FRAME:
        frame['number'] = frame_number(line)
        STATE, EXPECTED = STATE_FRAME, STATE_TIME
    elif STATE == STATE_FRAME and EXPECTED == STATE_TIME:
        frame['timecodes'] = frame_timecode(line)
        STATE, EXPECTED = STATE_TIME, STATE_CAPTION
    elif STATE == STATE_TIME and EXPECTED == STATE_CAPTION:
            caption = frame_caption(line)
            if caption == False:
                raise Exception("Caption expected. Blankline found")
            frame['caption'] = caption
            # It's first line of the caption and can't be blank
            STATE, EXPECTED = STATE_CAPTION, STATE_CAPTION
    elif STATE == STATE_CAPTION and EXPECTED == STATE_CAPTION: #
        caption = frame_caption(line, blank=True)
        if caption == True:
            # it's blankline, so do something!
            SUBTITLE.write(do(Frame(**frame))) # add it to the 
            STATE, EXPECTED = STATE_BLANK, STATE_FRAME
        else:
            frame['caption'] += "\n%s" % caption



SUBTITLE.write("\n\t\n\t\n")
SUBTITLE.close()
