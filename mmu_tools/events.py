import requests
from bs4 import BeautifulSoup
import tkinter as tk
import webbrowser

def fetch_event_headlines():
    url = "https://www.mmu.edu.my/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    headlines = []
    articles = soup.find_all('div', class_='col-md-4 col-sm-6')
    for article in articles:
        title_element = article.find('h3')
        if title_element:
            headline = title_element.get_text(strip=True)
            link = article.find('a')['href']
            headlines.append((headline, link))
    
    return headlines

def populate_headlines(headlines):
    for idx, (headline, _) in enumerate(headlines):
        y1 = idx * 40 + 20
        y2 = y1 + 30
        canvas.create_rectangle(10, y1, 590, y2, outline='#1d536e', width=2)
        text_id = canvas.create_text(20, (y1 + y2) // 2, anchor='w', text=headline, font=('Helvetica', 12), fill='#1d536e')
        canvas.tag_bind(text_id, '<Button-1>', lambda event, url=event_headlines[idx][1]: open_url(url))

def open_url(url):
    webbrowser.open_new_tab(url)

root = tk.Tk()
root.title("MMU Event Headlines")
root.geometry("600x400")

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

title_label = tk.Label(root, text="MMU Latest Event", font=('Helvetica', 16, 'bold'), pady=10, bg='#1d536e', fg='white')
title_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

canvas = tk.Canvas(root, bg='#f8f6f0', scrollregion=(0, 0, 600, 800))
canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
canvas.configure(yscrollcommand=scrollbar.set)

event_headlines = fetch_event_headlines()
populate_headlines(event_headlines)

root.mainloop()
