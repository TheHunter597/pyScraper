def get_links(products):
    links = []
    for product in products:
        link = product.find("a")
        if link:
            link = link.get("href")
            links.append("https://www.amazon.com" + link)
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


def extract_meta(data):
    title = data.find("span", id="productTitle").text.strip()
    image = data.find("img", class_="a-dynamic-image")["src"]
    try:
        price = data.find("span", class_="a-price").findChild("span").text
    except:
        price = data.find("span", class_="a-price-whole").findChild("span").text
    try:
        productDescriptionElements = data.find(
            "ul", class_="a-unordered-list a-vertical a-spacing-mini"
        ).findChildren("span", class_="a-list-item")
    except:
        print("mango herere")
    productDescription = ""
    for element in productDescriptionElements:
        productDescription += element.text + ", "
    return {
        "title": title,
        "price": price,
        "image": image,
        "description": productDescription,
    }
