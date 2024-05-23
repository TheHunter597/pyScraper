from bs4 import BeautifulSoup
import requests
import time
import json
import os
from utils.reviews_retriever import extract_reviews
from utils.product_retriever import extract_features, extract_meta, get_links
from utils.http_configs.proxy_servers import get_proxies
from utils.do_request import do_request

scrapingData = {}

with open(f"{os.path.dirname(os.path.realpath(__file__))}/scrapingData.json") as file:
    scrapingData = json.load(file)

outputFileName = scrapingData["outputFile"]


links = []

user_agents = scrapingData["userAgents"]
proxy_servers = get_proxies(scrapingData["threads"])


# def get_next_page(data):
#     pagination = data.find("span", class_="s-pagination-strip")
#     nextPage = pagination.findChild("a", class_="s-pagination-next")
#     nextPage = nextPage.get("href")
#     url = "https://www.amazon.com" + nextPage
#     return url


#######
productsData = []
count = 0
total_count = 0
#######
output_file_dir = f"{os.path.dirname(os.path.realpath(__file__))}/data/{outputFileName}"
os.makedirs(f"{os.path.dirname(os.path.realpath(__file__))}/data", exist_ok=True)


def main(index):
    global count
    global productsData
    global proxy_servers
    global user_agents
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": user_agents[index],
    }
    proxy = proxy_servers[index]

    if count >= scrapingData["count"]:
        return
    url = links[index]
    data = do_request(url, index, headers, proxy, user_agents, scrapingData)

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
            response = requests.get(
                link,
                headers=headers,
                proxies={
                    "http": "http://" + proxy,
                },
            )
            data = BeautifulSoup(response.text, "lxml")
            featuresData = extract_features(data)
            reviewsData = extract_reviews(data)
            meta = {}
            try:
                meta = extract_meta(data)
            except:
                print(link)
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
            if count < scrapingData["count"]:
                productsData.append(current_product_data)
                count += 1
                print(f"Total products scraped: {count} / {scrapingData['count']}")
                print("--------------------------")

                if scrapingData["accumulateAndWriteOnce"] == False:
                    with open(
                        output_file_dir,
                        "w",
                    ) as file:
                        file.write(json.dumps(productsData, indent=4))
                        file.close()

                time.sleep(scrapingData["secondsPerProduct"])

        except Exception as e:
            print(e)

            continue

    index += scrapingData["threads"]
    main(index)


from utils.start_threads import start

start(scrapingData, main, links)

if scrapingData["accumulateAndWriteOnce"] == True:
    outputFileName = scrapingData["outputFile"]
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/data/{outputFileName}", "w"
    ) as file:
        file.write(json.dumps(productsData, indent=4))
