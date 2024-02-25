# %%
from exif import Image

with open("../../data/IMG_3140.jpeg", "rb") as palm_1_file:
    palm_1_image = Image(palm_1_file)

with open("../../data/IMG_3149.jpeg", "rb") as palm_2_file:
    palm_2_image = Image(palm_2_file)

images = [palm_1_image, palm_2_image]
# %%
"""
Check if the picture has EXIF metadata
"""
for index, image in enumerate(images):
    if image.has_exif:
        status = f"contains EXIF (version {image.exif_version}) information."
    else:
        status = "does not contain any EXIF information."
    print(f"Image {index} {status}")
# %%
"""
Returns the metadata members in the file, such as creation date, latitude, longitude,altitude, information about the device that took the picture and more.
"""

image_members = []

for image in images:
    image_members.append(dir(image))

for index, image_member_list in enumerate(image_members):
    print(f"Image {index} contains {len(image_member_list)} members:")
    print(f"{image_member_list}\n")

# %%
"""
Prints the metadata members the pictures have in common
"""
common_members = set(image_members[0]).intersection(set(image_members[1]))
print(f"Image 0 and Image 1 have {len(common_members)} members in common:")
common_members_sorted = sorted(list(common_members))
print(f"{common_members_sorted}")

# %%
"""
Prints the device model that took the picture
"""
for index, image in enumerate(images):
    print(f"Device information - Image {index}")
    print("----------------------------")
    print(f"Make: {image.make}")
    print(f"Model: {image.model}\n")
# %%
"""
Prints additional information about the device model
"""
for index, image in enumerate(images):
    print(f"Lens and OS - Image {index}")
    print("---------------------")
    print(f"Lens make: {image.get('lens_make', 'Unknown')}")
    print(f"Lens model: {image.get('lens_model', 'Unknown')}")
    print(f"Lens specification: {image.get('lens_specification', 'Unknown')}")
    print(f"OS version: {image.get('software', 'Unknown')}\n")
# %%
"""
Prints the date the picture was taken
"""
for index, image in enumerate(images):
    print(f"Date/time taken - Image {index}")
    print("-------------------------")
    print(
        f"{image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}\n"
    )

# %%
"""
Prints the latitude and longitude where the picture was taken
"""
for index, image in enumerate(images):
    print(f"Coordinates - Image {index}")
    print("---------------------")
    print(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
    print(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}\n")
# %%
"""
Prints the latitude and longitude of where the pictures were taken
"""


def format_dms_coordinates(coordinates):
    return f"{coordinates[0]}° {coordinates[1]}' {coordinates[2]}\""


def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600

    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees

    return decimal_degrees


for index, image in enumerate(images):
    print(f"Coordinates - Image {index}")
    print("---------------------")
    print(
        f"Latitude (DMS): {format_dms_coordinates(image.gps_latitude)} {image.gps_latitude_ref}"
    )
    print(
        f"Longitude (DMS): {format_dms_coordinates(image.gps_longitude)} {image.gps_longitude_ref}\n"
    )
    print(
        f"Latitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)}"
    )
    print(
        f"Longitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)}\n"
    )

# %%
"""
Returns the location the pictures were taken using google maps

Opens a new tab for each location
"""


def draw_map_for_location(latitude, latitude_ref, longitude, longitude_ref):
    import webbrowser

    decimal_latitude = dms_coordinates_to_dd_coordinates(latitude, latitude_ref)
    decimal_longitude = dms_coordinates_to_dd_coordinates(longitude, longitude_ref)
    url = f"https://www.google.com/maps?q={decimal_latitude},{decimal_longitude}"
    webbrowser.open_new_tab(url)


for index, image in enumerate(images):
    draw_map_for_location(
        image.gps_latitude,
        image.gps_latitude_ref,
        image.gps_longitude,
        image.gps_longitude_ref,
    )

# %%
"""
Returns the location the pictures were taken using google maps

Opens a new tab for each location
"""

import reverse_geocoder as rg
import pycountry

for index, image in enumerate(images):
    print(f"Location info - Image {index}")
    print("-----------------------")
    decimal_latitude = dms_coordinates_to_dd_coordinates(
        image.gps_latitude, image.gps_latitude_ref
    )
    decimal_longitude = dms_coordinates_to_dd_coordinates(
        image.gps_longitude, image.gps_longitude_ref
    )
    coordinates = (decimal_latitude, decimal_longitude)
    location_info = rg.search(coordinates)[0]
    location_info["country"] = pycountry.countries.get(alpha_2=location_info["cc"])
    print(f"{location_info}\n")

# %%

