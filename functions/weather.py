import requests

def fetch_weather_report():
    def get_ipv6_address():
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data.get('ip')

    def get_location(ip):
        response = requests.get(f"https://ipinfo.io/{ip}")
        data = response.json()
        return data['city']

    ipv6 = get_ipv6_address()
    if ipv6:
        location = get_location(ipv6)
        if location:
            url = f"http://wttr.in/{location}?format=j1"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and 'current_condition' in data:
                current_condition = data['current_condition'][0]
                temp_c = current_condition['temp_C']
                description = current_condition['weatherDesc'][0]['value']
                return f"The current weather in {location} is {temp_c}°C, {description}."
            else:
                return "Could not retrieve weather data."
        else:
            return "Could not determine location."
    else:
        return "Could not retrieve IP address."
