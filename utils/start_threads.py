import concurrent.futures
import re


def start(scrapingData, main, links):
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=scrapingData["threads"]
    ) as executor:
        original = scrapingData["url"]
        for i in range(50):
            if original.find("&crid") != -1:
                result = re.sub(r"&crid", f"&page={i+1}&crid", original)
                links.append(result)
            elif original.find("page=") != -1:
                result = re.sub(r"page=\d+", f"page={i+1}", original)
                links.append((result))
            else:
                with_pages = original.split("&")
                with_pages.insert(2, f"page={i+1}")
                links.append("&".join(with_pages))
        result = [i for i in range(scrapingData["threads"])]
        executor.map(main, result)
