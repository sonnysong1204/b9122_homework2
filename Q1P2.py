'''
Crawl the press room of the European Parliament and extract at least 10 press
releases that cover the plenary sessions and contain the word "crisis".
'''

import os

# Change the current working directory to the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

from bs4 import BeautifulSoup
import urllib.request


seed_url = "https://www.europarl.europa.eu/news/en/press-room"

urls = [seed_url]  # queue of urls to crawl
seen = [seed_url]  # stack of urls seen so far
press_releases_found = 0  # count of press releases containing the word "crisis"

# Keep accessing URLs until we find 10 press releases that satisfy the criteria
while len(urls) > 0 and press_releases_found < 10:
    curr_url = urls.pop(0)
    try:
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        content_type = response.headers.get('Content-Type')
        
        # If the content type is not HTML, skip this URL and print a message
        if 'html' not in content_type:
            print(f"Oops, we encountered a web page that is not using HTML at {curr_url}. Skipping...")
            continue

        webpage = response.read()
        soup = BeautifulSoup(webpage, "html.parser")

        # Check if the page is related to plenary sessions
        plenary_session_tag = soup.find('span', {'class': 'ep_name'}, string="Plenary session")
        if plenary_session_tag:
            # Check if the press release contains the word "crisis"
            if "crisis" in soup.get_text().lower():
                press_releases_found += 1
                # Save the HTML source to a .txt file
                with open(f"2_{press_releases_found}.txt", "w", encoding="utf-8") as file:
                    file.write(str(soup))

        # Add new URLs to the queue
        for tag in soup.find_all('a', href=True):
            child_url = tag['href']
            absolute_url = urllib.parse.urljoin(seed_url, child_url)
            # startswith is used to suppress the crawler from accessing social media links inside the pages
            # without this, the crawler will try to access Twitter links, which is not what we want 
            if absolute_url.startswith(seed_url) and absolute_url not in seen:
                urls.append(absolute_url)
                seen.append(absolute_url)

    except Exception as ex:
        print(f"Error accessing {curr_url}: {ex}")
        continue

print(f"Saved {press_releases_found} press releases covering the plenary sessions and containing the word 'crisis'.")
