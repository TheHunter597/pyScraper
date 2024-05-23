import os
import requests
import random


def get_proxies(count):
    result = []
    import json

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/proxy_servers.json",
        "r",
    ) as file:
        servers = json.load(file)
        random.shuffle(servers)
        file.close()

    for server in servers:
        print("trying", server)
        if len(result) == count:
            return result
        try:
            response = requests.get(
                "https://www.google.com/",
                proxies={
                    "http": "http://" + server,
                },
                headers=headers,
                timeout=5,
            )

            if response.status_code == 200:
                print(response.status_code, "succeeded")
                result.append(server)
        except requests.RequestException as e:
            print(server + " failed")
            print(str(e))
            continue
    return result
