import math
import galah
import pandas as pd

pd.set_option('display.max_rows', None)  # None means no limit
pd.set_option('display.max_columns', None)  # None means no limit

# Set up configuration for the galah library
galah.galah_config(email="samcaton92@gmail.com")
galah.galah_config()

# Define the center of your bounding box
center_longitude = 152.93173217773438
center_latitude = -27.10943603515625

# Define the radius in meters
radius_meters = 500

# Latitude to meters conversion
degree_to_meters = 111000  # meters per degree of latitude

# Convert radius to degrees
radius_degrees_latitude = radius_meters / degree_to_meters

# Longitude to meters conversion
def longitude_degrees_per_meter(latitude):
    return 111000 * math.cos(math.radians(latitude))

# Calculate the conversion for the current latitude
longitude_distance_per_degree = longitude_degrees_per_meter(center_latitude)

# Convert radius to degrees for longitude
radius_degrees_longitude = radius_meters / longitude_distance_per_degree

# Defines the bounding box with a 100-meter radius
bbox = {
    "xmin": center_longitude - radius_degrees_longitude,   # min longitude
    "ymin": center_latitude - radius_degrees_latitude,    # min latitude
    "xmax": center_longitude + radius_degrees_longitude,   # max longitude
    "ymax": center_latitude + radius_degrees_latitude    # max latitude
}

# Define filters
filters = ["year>=2010", "year<=2024"]

# Retrieve data with bounding box and filters
atlas_output = galah.atlas_species(
    filters=filters,
    bbox=bbox  # Using dictionary for bounding box
)

# Print to the console
print(atlas_output)

# Print to a file
atlas_output.to_csv('dataframe_output.csv', index=False)
