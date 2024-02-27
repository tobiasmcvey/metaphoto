# %%
import os

from get_metadata import (
    get_exif,
    get_exif_ifd,
    get_created_time,
    clean_datestamps,
    just_dates,
)

# %%
images = []
target_dir = "../../data/pictures/"
files = os.listdir(target_dir)
# %%
# this works for a single file
exif = get_exif(target_dir, "IMG_0763.jpeg")
d = get_exif_ifd(exif)

# %%
# works for a list of files
data = []
for i in files:
    exif = get_exif(target_dir, i)
    ifd = get_exif_ifd(exif)
    data.append(ifd)

# %%
ctime = get_created_time(data=data)
# %%
cleaned = clean_datestamps(data=ctime)
# %%
dates = just_dates(data=cleaned)
# %%
# Next: append created date to filename
# %%
for x, y in zip(files, dates):
    source = target_dir + x
    destination = target_dir + y.strftime("%Y-%m-%d") + "-" + x
    os.rename(source, destination)
# %%
os.listdir(target_dir)  # print list of new filenames
# %%
