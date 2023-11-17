from selenium import webdriver
from mongo import get_database
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
database = get_database()

# Collection where stores all links with the brands links
brands_link_collection = database["brands_link_list"]

# Collection where stores all brands links in the "brands_link_collection"
brands_collection = database["brands_link"]

# Collection where stores all unique brands in the "brands_collection"
unique_brands_collection = database["unique_brands"]

# Collection where stores all unique perfumes from the brands in the "unique_brands_collection"
prefume_links_collection = database["perfume_link"]

API_KEY = "YOUR_API"

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

def get_link_with_proxy(url : str):
    return f"http://api.scraperapi.com?api_key={API_KEY}&url={url}"

def load_brands_link() -> list:
    driver.get("https://www.fragrantica.com.br/designers-1/#A")

    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y", "Z"]
    links = []
    to_return = []

    for letter in alphabet:
        driver.implicitly_wait(10)
        links.append(str(driver.find_element(By.XPATH, f"//a[contains(text(), '{letter}')]").get_attribute('href')))
        driver.implicitly_wait(10)

    for link in links:
        if link[:40] == "https://www.fragrantica.com.br/designers":
            to_return.append({"link" : link})

    brands_link_collection.insert_many(to_return)
    return to_return

def load_brands():
    links = [i['link'] for i in brands_link_collection.find()]


    for link in links:
        driver.get(get_link_with_proxy(link))
        driver.implicitly_wait(10)

        html = driver.page_source
        soup = BeautifulSoup(html)

        brands = soup.find_all("div", {"class": "designerlist cell small-6 large-4"})

        for i in brands:
            brand_link = i.a['href']
            brand_name = i.a.get_text()
            document = {
                "link" : brand_link,
                "name" : brand_name
            }
            brands_collection.insert_one(document)

        time.sleep(3)

def remove_duplicates_brands_link():
    unique_brands = brands_collection.distinct("link")

    for i in unique_brands:
        brand = brands_collection.find_one({
            'link' : i
        })

        unique_brands_collection.insert_one({
            'name' : brand['name'],
            'link' : brand['link']
        })        

def load_perfume_links():
    brands = list(unique_brands_collection.find())[4996:]
    count = 4996
    
    for brand in brands:
        url = f"https://www.fragrantica.com.br/{brand['link']}#all-fragrances"

        driver.get(get_link_with_proxy(url))
        soup = BeautifulSoup(driver.page_source, features="html.parser")

        print(f"{bcolors.OKGREEN } Marca numero : {count}{brand['name']} {bcolors.ENDC}")
        count += 1

        perfumes = soup.find_all("div", {"class": "cell text-left prefumeHbox px1-box-shadow"})

        for i in perfumes:
            spans = i.find_all('span')
            sex = spans[-2].get_text()
            year = spans[-1].get_text()

            top = i.find("div", {"class": "flex-child-auto"})

            link = top.h3.a["href"]
            name = top.h3.get_text()

            document = {
                "name" : name.split("\n")[1],
                "link" : link,
                "sex" : sex,
                "year" : year,
                "brand_name" : brand['name'],
                "brand_link" : brand['link'],
                "scrapped" : False
            }

            prefume_links_collection.insert_one(document)

            print(document)
            print("-="*15)

def teste():
    brands = list(unique_brands_collection.find())[4996:]
    print(brands[0]['name'])
    print(len(brands))
    # for index, brand in enumerate(brands):
    #     if brand['link'] == '/desenhista/Velvet-Sweet-Pea-s-Purrfumery.html':
    #         print(index)
    #         print(brand['name'])


if __name__ == "__main__":
    load_perfume_links()
    # teste()
    a = input()
    driver.close()