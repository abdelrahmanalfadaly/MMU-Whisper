import folium
import openrouteservice as ors

# Initialize the OpenRouteService client with the correct API key
client = ors.Client(key='5b3ce3597851110001cf6248b04254c054a4456786e8b46bcf6ce183')

# Create a folium map centered on the specified location
m = folium.Map(location=[2.9277371755465396, 101.6420648217607], tiles="cartodbpositron", zoom_start=13)

# Coordinates from FCI to lecture complex
coords = [[101.64169074928611, 2.928525546328487], [101.64207031686595, 2.9280650208917507]]

# Fetch the route using OpenRouteService
route = client.directions(coordinates=coords, profile='foot-walking', format='geojson')

# Extract coordinates from the route for the polyline
route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]

# Add the route to the map
folium.PolyLine(locations=route_coords, color='blue').add_to(m)

# Save the map to an HTML file
m.save('route_map.html')
