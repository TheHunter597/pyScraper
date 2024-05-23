import requests
from bs4 import BeautifulSoup


def do_request(url, index, headers, proxy, user_agents, scrapingData):
    try:
        print(headers)
        response = requests.get(
            url,
            headers=headers,
            proxies={
                "http": "http://" + proxy,
            },
            timeout=5,
        )
        headers["User-Agent"] = user_agents[index % scrapingData["threads"]]
        current = index + 1
        while (
            response.status_code != 200
            or response.text.find("To discuss automated access") != -1
        ):

            headers["User-Agent"] = user_agents[current]
            print(f"Changing user agent to { user_agents[current]}")
            print("-------------------------")
            current += scrapingData["threads"]
            response = requests.get(url, headers=headers)

        print(response.status_code)
        print(f"Scraping {url}")

        return BeautifulSoup(response.text, "lxml")
    except Exception as e:
        print(e)
