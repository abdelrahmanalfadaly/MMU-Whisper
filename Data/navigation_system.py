import folium
from folium import plugins
import json
import os

# Function to print directory contents for debugging
def print_directory_contents(path):
    for root, dirs, files in os.walk(path):
        print(root)
        for file in files:
            print(f"  {file}")

# Print current directory contents
print("Current directory contents:")
print_directory_contents(".")

# Define MMU location coordinates (latitude, longitude)
MMUlocation = (2.929940812828235, 101.64239554844073)

# Initialize the map centered on MMU
map_MMU = folium.Map(location=MMUlocation, width="75%", zoom_start=17)

# Load and add the FOM geojson file to the map
FCIOutline = 'CampusNavigator/GeoResources/FCI.geojson'
try:
    with open(FCIOutline, 'r') as file:
        FOM_geojson = json.load(file)
    folium.GeoJson(FOM_geojson, name="FOM").add_to(map_MMU)
except FileNotFoundError:
    print(f"File not found: {FCIOutline}")

# Load and add the FCI-lecture_complex geojson file to the map
testGeoJson = 'CampusNavigator/GeoResources/path/FCI-lecture_complex.geojson'
try:
    with open(testGeoJson, 'r') as file:
        testWay = json.load(file)
except FileNotFoundError:
    print(f"File not found: {testGeoJson}")

# Function to switch latitude and longitude in coordinates
def switchPosition(coordinate):
    return [coordinate[1], coordinate[0]]

# Switch the coordinates for each feature in the GeoJSON
for feature in testWay.get('features', []):
    if feature['geometry']['type'] == 'LineString':
        feature['geometry']['coordinates'] = [switchPosition(coord) for coord in feature['geometry']['coordinates']]
    elif feature['geometry']['type'] == 'Polygon':
        feature['geometry']['coordinates'] = [[switchPosition(coord) for coord in ring] for ring in feature['geometry']['coordinates']]

# Add the updated GeoJSON to the map
folium.GeoJson(testWay, name="FCI Lecture Complex Path").add_to(map_MMU)

# Coordinates for AntPath (example path)
ant_path_coords = [
    [2.928459845810437, 101.64169268904601],
    [2.9282124007676913, 101.64169613027553],
    [2.9281453843929626, 101.64193357516001],
    [2.9280577458447254, 101.64207638600737],
    [2.928459845810437, 101.64169268904601],
    [2.9282124007676913, 101.64169613027553],
    [2.9281453843929626, 101.64193357516001],
    [2.9280577458447254, 101.64207638600737]
]

# Add AntPath to the map
plugins.AntPath(ant_path_coords).add_to(map_MMU)

# Display the map
map_MMU
