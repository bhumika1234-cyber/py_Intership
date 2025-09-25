

import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

response = requests.get(URL)
if response.status_code != 200:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    exit()

html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

headlines = []
for tag in soup.find_all(['h2', 'h3']):
    title = tag.get_text(strip=True)
    if title and len(title) > 20:  
        headlines.append(title)

with open("headlines.txt", "w", encoding="utf-8") as file:
    for i, headline in enumerate(headlines, start=1):
        file.write(f"{i}. {headline}\n")

print(f"✅ Scraped {len(headlines)} headlines and saved to 'headlines.txt'")