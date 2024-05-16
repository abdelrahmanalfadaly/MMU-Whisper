# https://www.google.com/search?q=weather+cyberjaya&sca_esv=74c740cd3a771c52&sca_upv=1&rlz=1C1ONGR_enMY1071MY1071&sxsrf=ADLYWILyUFCLXq8RV4jtbY4gKzG4A_RGXg%3A1715189228016&ei=7LU7Zv9Tjonj4Q-T-o0I&oq=weather+cyb&gs_lp=Egxnd3Mtd2l6LXNlcnAiC3dlYXRoZXIgY3liKgIIADINEAAYgAQYywEYRhiAAjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMgoQABiABBgKGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMhkQABiABBjLARhGGIACGJcFGIwFGN0E2AEBSJMbUP4BWLENcAF4AZABAJgBYaABigOqAQE1uAEByAEA-AEBmAIHoAKnD8ICChAAGLADGNYEGEfCAgoQABiABBhDGIoFwgILEAAYgAQYkgMYigXCAgsQABiABBjJAxjLAcICDhAuGIAEGNEDGMcBGMsBmAMAiAYBkAYKugYGCAEQARgTkgcHNS4xLjctMaAHwxY&sclient=gws-wiz-serp
# user agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36

# span   id = wob_tm
import requests
from bs4 import BeautifulSoup

def get_weather(location):
    query = location.replace(" ", "+")  # Replace spaces with + in the query
    url = f'https://www.google.com/search?q=weather+{query}&u=c'  # Add &u=c to ensure the temperature is in Celsius
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            temp = soup.find('span', id='wob_tm').text
            desc = soup.find('span', id='wob_dc').text
            return f"{temp}°C {desc}"
        else:
            return "Error: Unable to fetch weather information"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
location = "Cyberjaya"
print(get_weather(location))
