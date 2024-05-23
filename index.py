from bs4 import BeautifulSoup
import requests
import time
import json
import os
from utils.reviews_retriever import extract_reviews
from utils.product_retriever import extract_features, extract_meta, get_links
import concurrent.futures

scrapingData = {}

with open(f"{os.path.dirname(os.path.realpath(__file__))}/scrapingData.json") as file:
    scrapingData = json.load(file)

outputFileName = scrapingData["outputFile"]

if scrapingData["accumulateAndWriteOnce"] == True and scrapingData["threads"] > 1:
    print(
        "Currently you cant use AccumulateAndWriteOnce and more than 1 thread at the same time"
    )
    exit()

links = [
    scrapingData["url"],
]

user_agents = scrapingData["userAgents"]
current_user_agent = 0

headers = {
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "User-Agent": user_agents[current_user_agent],
}


def do_request(url, index):
    headers["User-Agent"] = user_agents[index % scrapingData["threads"]]
    try:
        global current_user_agent
        response = requests.get(url, headers=headers)
        while response.status_code != 200:
            current_header = user_agents[current_user_agent]
            headers["User-Agent"] = current_header
            print(f"Changing user agent to {current_header}")
            current_user_agent += 1
            response = requests.get(url, headers=headers)
        print(response.status_code)
        print(f"Scraping {url}")

        return BeautifulSoup(response.text, "lxml")
    except Exception as e:
        print(e)


def get_next_page(data):
    pagination = data.find("span", class_="s-pagination-strip")
    nextPage = pagination.findChild("a", class_="s-pagination-next")
    nextPage = nextPage.get("href")
    url = "https://www.amazon.com" + nextPage
    return url


#######
productsData = []
count = 0
total_count = 0
#######
output_file_dir = f"{os.path.dirname(os.path.realpath(__file__))}/data/{outputFileName}"
os.makedirs(f"{os.path.dirname(os.path.realpath(__file__))}/data", exist_ok=True)


def main(index):
    if count >= scrapingData["count"]:
        return
    global count
    global productsData
    url = links[index]
    data = do_request(url, index)
    links.append(get_next_page(data))

    products = data.find_all(
        "div",
        class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16",
    )
    if len(products) == 0:
        products = data.find_all(
            "div",
            class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20",
        )
    productsLinks = get_links(products)
    print("--------------------------")

    for link in productsLinks:

        try:
            if count >= scrapingData["count"]:
                break
            response = requests.get(link, headers=headers)
            data = BeautifulSoup(response.text, "lxml")

            featuresData = extract_features(data)
            reviewsData = extract_reviews(data)
            meta = extract_meta(data)
            current_product_data = {
                "title": meta["title"],
                "price": meta["price"],
                "image": meta["image"],
                "features": featuresData,
                "description": meta["description"],
                "reviews": reviewsData,
            }
            ## checks if --features command line argument is passed if yes then product must have features
            if scrapingData["mustHaveFeatures"] == True:
                if len(featuresData) == 0:
                    print(
                        f"Skipping product number {total_count} as it does not have features"
                    )
                    continue
            if scrapingData["mustHaveReviews"] == True:
                if len(reviewsData) == 0:
                    print(
                        f"Skipping product number ${total_count} as it does not have reviews"
                    )

                    continue
            productsData.append(current_product_data)
            if scrapingData["accumulateAndWriteOnce"] == False:
                with open(
                    output_file_dir,
                    "w",
                ) as file:
                    file.write(json.dumps(productsData, indent=4))
                    file.close()

            count += 1

            print(f"Total products scraped: {count} / {scrapingData['count']}")
            print("--------------------------")

            time.sleep(scrapingData["secondsPerProduct"])

        except Exception as e:
            print(e)

            continue

    index += scrapingData["threads"]
    main(index)


with concurrent.futures.ThreadPoolExecutor(
    max_workers=scrapingData["threads"]
) as executor:
    import re

    original = scrapingData["url"]
    for i in range(scrapingData["threads"] + 1):
        if original.find("page=") != -1:
            result = re.sub(r"page=\d+", f"page={i+1}", original)
            links.append((result))
        else:
            with_pages = original.split("&")
            with_pages.insert(2, f"page={i+1}")
            links.append("&".join(with_pages))
    links.pop(0)
    result = [i for i in range(scrapingData["threads"])]
    executor.map(main, result)

if scrapingData["accumulateAndWriteOnce"] == True:
    outputFileName = scrapingData["outputFile"]
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/data/{outputFileName}", "w"
    ) as file:
        file.write(json.dumps(productsData, indent=4))
