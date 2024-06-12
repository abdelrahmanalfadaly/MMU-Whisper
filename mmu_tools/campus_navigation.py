import re
import webbrowser

MMU_Places = {
    "library": "Siti Hasmah Digital Library",
    "fci": "fci mmu"
}

def get_place_name(place):
    return MMU_Places.get(place.lower(), place)

def extract_directions(input_text):
    pattern = r'from\s+(.*?)\s+to\s+(.*)'
    match = re.search(pattern, input_text, re.IGNORECASE)
    
    if match:
        origin = match.group(1).strip()
        destination = match.group(2).strip()
        return get_place_name(origin), get_place_name(destination)
    return None, None

def create_google_maps_url(origin, destination):
    origin = origin.replace(' ', '+')
    destination = destination.replace(' ', '+')
    url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"
    return url

def main():
    user_input = input("Enter your direction query: ")
    origin, destination = extract_directions(user_input)
    
    if origin and destination:
        url = create_google_maps_url(origin, destination)
        print(f"Google Maps URL: {url}")
        webbrowser.open(url)
    else:
        print("Couldn't detect a valid direction query.")

if __name__ == "__main__":
    main()
