import requests
from mongo import get_database
from queue import Queue 
import threading
from bs4 import BeautifulSoup 
import json
from requests_html import HTMLSession
import time


db = get_database()
perfume_links_collection = db["perfume_link"]

perfumes_queue = Queue()

API_KEY = "c291cbb770da2844c4835b9ee44d8914"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# def get_link_with_proxy(url : str):
#     return f"http://api.scraperapi.com?api_key={API_KEY}&url={url}"

def load_perfumes_to_scrape(batch_size : int):
    # print(perfume_links_collection.find({"scrapped" : False})[0])
    index_test = 0
    for i in perfume_links_collection.find({"scrapped" : False}):
        perfumes_queue.put(i)

        index_test += 1

        if index_test > batch_size:
            break


def scrape_perfume():
    global perfumes_queue
    global thread_index

    while not perfumes_queue.empty():
        start_time = time.time()

        perfume = perfumes_queue.get()

        URL = f"https://www.fragrantica.com.br{perfume['link']}"
        # URL = "https://www.fragrantica.com.br/perfume/O-Boticario/Quasar-Brave-53752.html"

        proxies = {
        "http": f"http://scraperapi:{API_KEY}4@proxy-server.scraperapi.com:8001",
        "https": f"http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001"
        }

        page = requests.get(URL, proxies=proxies, verify=False)

        soup = BeautifulSoup(page.text, "html.parser")

        # Rating of the perfume, example: 4 of 15000 votes(range between 1 to 5)
        rating = soup.find("span", {"itemprop" : "ratingValue"}).get_text()
        number_of_votes = soup.find("span", {"itemprop" : "ratingCount"}).get_text()

        # Accords of the perfume(categories) perfume like: citrus, iris, lether
        accord_bars = soup.find_all("div", {"class" : "accord-bar"})
        accords = [
            {
                "accord_name" : i.get_text(),
                "porcentage" : i['style'].split(";")[-3][9:]
            } for i in accord_bars
        ]

        try:
            notes_bars = soup.find("div", {"id" : "pyramid"}).div.div.find_all("h4")[0].parent.find_all("pyramid-level")

            top_notes_links = notes_bars[0].find_all("a")
            middle_notes_links = notes_bars[1].find_all("a")
            base_notes_links = notes_bars[2].find_all("a")

            top_notes = [i.parent.get_text() for i in top_notes_links]
            middle_notes = [i.parent.get_text() for i in middle_notes_links]
            base_notes = [i.parent.get_text() for i in base_notes_links]
        except Exception:
            top_notes = []
            middle_notes = []
            base_notes = []


        # Create document and save on mongo
        document = {
            "name" : perfume['name'],
            "link": perfume['link'],
            "sex" : perfume['sex'],
            "year" : perfume['year'],
            "rating" : rating,
            "number_of_votes" : number_of_votes,
            "accords" : accords,
            "top_notes" : top_notes,
            "middle_notes" : middle_notes,
            "base_notes" : base_notes,

        }

        # Log everithing
        execution_time = time.time() - start_time
        print(f"{bcolors.HEADER}{'-='*60}{bcolors.ENDC}")
        print(f"{bcolors.WARNING}--- {'%.3f' % execution_time} seconds ---{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}{document}{bcolors.ENDC}")

    

# URL = "https://realpython.github.io/fake-jobs/"
# page = requests.get(URL)

# print(page.text)

if __name__ == '__main__':
    load_perfumes_to_scrape(0)
    scrape_perfume()
    print(f"{bcolors.HEADER}{'-='*60}{bcolors.ENDC}")
    # threading.Thread(target=scrape_perfume).start()
    # threading.Thread(target=scrape_perfume).start()
    # scrape_perfume()