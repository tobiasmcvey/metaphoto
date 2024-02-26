# %%
import os
import datetime
import dateutil.parser

from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS

"""
This program can read metadata from pictures

It can be used to 
* Find out when the picture was taken
* Find out where the picture was taken
* Find out what device model took the picture, and which camera was used

and
* Append the creation date to the filename


The program currently works for pictures

These are the tags that can be extracted
https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

Inspired by this thread
https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil

TODO add parser so it can be run as a command line tool
TODO make the program work for video as well
"""
# %%
images = []
target_dir = "../../data/pictures/"
files = os.listdir(target_dir)


# %%
def get_exif(target_dir, file_name) -> Exif:
    """
    Get EXIF data for a single image
    """
    image: Image.Image = Image.open(target_dir + file_name)
    return image.getexif()


# %%


def get_exif_ifd(exif):
    """
    Get the IFD - image file directories - for a single image
    """
    for key, value in TAGS.items():
        if value == "ExifOffset":
            break
    info = exif.get_ifd(key)
    return {TAGS.get(key, key): value for key, value in info.items()}


# %%
# this works for a single file
exif = get_exif(target_dir, "IMG_0763.jpeg")
d = get_exif_ifd(exif)
d

# %%
# works for a list of files
data = []
for i in files:
    exif = get_exif(target_dir, i)
    ifd = get_exif_ifd(exif)
    data.append(ifd)
# %%
"""
The data we are looking for is in the field DateTimeOriginal
Retrieve it and convert it into datetime
Then created new filenames
"""

def get_created_time(data: list):
    """
    Get the date the picture was taken as a string
    """
    created_datestamps = []
    for i in data:
        created_datestamps.append(i["DateTimeOriginal"])  # got our data :D
    return created_datestamps
# %%
def clean_datestamps(data: list):
    """
    Converts the string into a datetime.datetime object
    """
    cleaned_datestamps = []
    for i in data:
        i = i.replace(":", "-", 2)
        i = i.replace(" ", "T", 1)
        cleaned_datestamps.append(
            dateutil.parser.isoparse(i)
        )  # converted the datetime into dates and time of day
    return cleaned_datestamps
# %%
def just_dates(data: list):
    """
    Converts the datetime.datetime object into a datetime.date object
    """
    just_dates = []
    for i in data:
        just_dates.append(datetime.datetime.date(i))
    return just_dates
# %%
ctime = get_created_time(data=data)
# %% 
cleaned = clean_datestamps(data=ctime)
# %%
dates = just_dates(data=cleaned)
# %%
# Next: append created date to filename
# %%
for x,y in zip(files, dates):
    source = target_dir + x
    destination = target_dir + y.strftime("%Y-%m-%d") + "-" + x
    os.rename(source, destination)
# %%
os.listdir(target_dir) # print list of new filenames
# %%
