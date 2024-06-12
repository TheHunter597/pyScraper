import re


def get_links(data):
    links = []
    products = []

    products = data.find_all(
        "div",
        class_=re.compile("s-result-item s-asin", re.I),
    )

    for product in products:
        try:
            header = product.find(
                "h2", class_=re.compile("a-size-mini a-spacing-none a-color-base", re.I)
            )

            link = header.find("a")
        except Exception as e:
            print(e)

        if link:
            href = link.get("href")
            if href.find("ref") != -1:
                modified_link = "https://www.amazon.com" + href.split("ref")[0]
                links.append(modified_link)
            else:
                links.append("https://www.amazon.com" + href)
    return links


def extract_features(data):
    featuresData = []
    featuresTable = data.find("table", class_="a-normal a-spacing-micro")
    try:
        features = featuresTable.findChildren("td", class_="a-span3")
    except:
        return []
    featuresDescription = featuresTable.findChildren("td", class_="a-span9")
    for i in range(len(features)):
        featuresData.append(
            {
                "name": features[i].findChild("span").text.strip(),
                "description": featuresDescription[i].findChild("span").text.strip(),
            }
        )

    return featuresData


def extract_price(data):
    try:
        price = data.find("span", class_="a-price").findChild("span").text
    except:
        price = data.find("span", class_="a-price-whole").findChild("span").text
    return price


def extract_image(data):
    image = data.find("img", id="landingImage")

    if image == None:
        image = data.find("img", id="main-image")

    return image["src"]


def extract_description(data):
    try:
        productDescription = ""
        product_description_list = data.find_all(
            "ul", class_=re.compile("a-unordered-list a-vertical", re.I)
        )
        if len(product_description_list) > 0:
            for list in product_description_list:
                current = list.find("li").find("span").text.strip()
                productDescription += current + ", "
        return productDescription
    except:
        return ""


def extract_meta(data):

    title = data.find("span", id="productTitle").text.strip()
    image = extract_image(data)
    price = extract_price(data)
    description = extract_description(data)
    return {
        "title": title,
        "price": price,
        "image": image,
        "description": description,
    }


def extract_product_details(data):
    try:
        container = data.find("div", id="prodDetails")
        container_tables = container.find_all("table")

        details_data = {}

        for table in container_tables:
            rows = table.find_all("tr")
            for row in rows:
                try:
                    key = row.find("th").text.strip()
                    value = row.find("td").text.strip()
                    details_data[key] = value
                except:
                    pass

        return details_data
    except:
        return {}
