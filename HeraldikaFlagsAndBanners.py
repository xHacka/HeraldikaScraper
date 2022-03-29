import requests
import time
import os
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from sys import argv, exit

verbose = False
if len(argv) > 1 and argv[1] == "-v": verbose = True

def download_images(domain):

    # Website HTML
    website = BS(requests.get(domain).text, 'lxml')

    # All The Links With Class arms_img (Meaning Flag/Banner Links)
    links = website.find_all('div', class_="arms_img")

    # Join The Links And Create Full Domain
    flag_links = [urljoin(url, str(links[i].a['href'])) for i in range(len(links))]
    
    # Scrape Flag URLs
    for flag_link in flag_links:

        # Visit The Flag/Banner Link
        images = BS(requests.get(flag_link).text, 'lxml')

        # Find All img Elements
        image_src = images.find('div', class_="armstxt").find_all('img')

        try:

            # Find The Image Links
            image_links = [image_src[i]['src'] for i in range(len(image_src))]

            # Join THe Links And Create Full Domain Links
            banner, flag = urljoin(url, image_links[0]), urljoin(url, image_links[1])

            # Grab The Names Of Images For Folder Names
            dir_name = image_links[0].split('/')[-1].split('.')[0]

            # Create Folders For Each Name
            os.makedirs('Heraldika/' + dir_name)

            # Download Images In Specified Folder
            with open(f'Heraldika/{dir_name}/{dir_name}-banner.png', 'wb') as f: f.write(requests.get(banner).content)
            with open(f'Heraldika/{dir_name}/{dir_name}-flag.png', 'wb') as f: f.write(requests.get(flag).content)

            # Download About Data 
            with open(f'Heraldika/{dir_name}/{dir_name}-data.txt', 'w', encoding="UTF-8") as f: 
                for tr in images.find('div', class_='armstxt').find_all('tr'):
                    f.write(tr.find_all('td')[-1].text)  

        except IndexError: continue
        except FileExistsError: continue
        except TimeoutError: print("[-] Connection Failed")
        except KeyboardInterrupt: print("[!] Exiting Program"); exit()


    # Find All Webpage Pages
    next_page = website.find('div', class_="navbar_in").find_all('a')

    # Join The Links For Full Domain
    next_page_link = urljoin(url, next_page[-1]['href'])

    # Create List For Visited Links
    if next_page_link not in next_page_links:
        if verbose: print(f"[+] Finished Downloading {domain}")
        next_page_links.append(next_page_link)

        # If Next Page Exists Call Function Again
        download_images(domain=next_page_link)


if __name__ == '__main__':
    print("[*] Starting Download")
    url, s = 'http://www.heraldika.ge/index.php?m=41&p_news=1', time.time()
    next_page_links = []
    download_images(domain=url)
    print('[*] Program Finished')
    print(f'[!] Elapsed Time {time.time() - s:.3f}s')
    exit()
