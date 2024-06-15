import re
import webbrowser

MMU_Places = {
"library": "Siti Hasmah Digital Library",
    "fci": "fci mmu",
    "foe": "Faculty of Engineering MMU Cyberjaya",
    "fom":"Faculty of Management (FOM) @ MMU Cyberjaya",
    "dtc":"Dewan Tun Canselor",
    "Misri Plaza":"Misri Plaza MMU Cyberjaya",
    "mph": "Multipurpose Hall (MPH) @ MMU Cyberjaya",
    "lecture hall":"Central Lecture Complex Cyberjaya",
    "he and she cafe":"He & She Coffee MMU Cyberjaya",
    "central plaza":"Central Plaza, MMU Cyberjaya",
    "hajitapah":"Restoran Haji Tapah Bistro Cyberjaya",
    "gallery":"E-Gallery MMU Cyberjaya",
    "cinema":"FCA Cinema MMU Cyberjaya",
    "fca":"Faculty of Cinematic Arts Cyberjaya",
    "fac":"Faculty of Applied Communication Cyberjaya",
    "fcm":"Faculty of Creative Multimedia (FCM) MMU Cyberjaya",
    "stad":"STAD Building MMU Cyberjaya",
    "deen's cafe":"Deen's Café MMU Cyberjaya",
    "ssc":"MMU Student Services Centre Cyberjaya",
    "sport complex":"MMU Indoor Sports Complex Cyberjaya",
    "starbees":"MMU Starbees Cyberjaya",
    "gym":"MMU Gym Cyberjaya",
    "stadium":"MMU Stadium Cyberjaya",
    "football field":"MMU Football Field Cyberjaya",
    "swimming pool":"MMU Swimming Pool Complex Cyberjaya",
    "mmu cyber park":"MMU Cyber Park Cyberjaya",
    "tekun mart":"TEKUN Mart MMU Cyberjaya",
    "hb4":"MMU Hostel HB4 Cyberjaya",
    "hb3":"MMU Hostel HB3 Cyberjaya",
    "hb2":"MMU Hostel HB2 Cyberjaya",
    "hb1":"MMU Hostel HB1 Cyberjaya",
    "ssc hostel":"SCC Hostel MMU Cyberjaya",
    "volleyball court":"MMU Volleyball Court Cyberjaya",
    "basketball court":"MMU Indoor Sports Complex Cyberjaya",
    "badminton court":"MMU Indoor Sports Complex Cyberjaya",
    "seven eleven MMU":"MMU Starbees Cyberjaya"

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
