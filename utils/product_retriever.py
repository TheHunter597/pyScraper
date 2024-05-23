def get_links(products):
    links = []
    for product in products:
        link = product.find(
            "h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2"
        ).findChild("a")

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
    image = ""
    try:
        image = data.find("img", id="landingImage")["src"]
    except:
        image = data.find("img", id="main-image")["src"]
    finally:
        if image == "":
            print("product dosent have an image")
    return image


def extract_meta(data):
    try:
        title = data.find("span", id="productTitle").text.strip()
    except Exception as e:
        print(e)
        print("no title found")
    image = extract_image(data)
    price = extract_price(data)

    try:
        productDescriptionElements = data.find(
            "ul", class_="a-unordered-list a-vertical a-spacing-mini"
        )
        if productDescriptionElements is not None:
            productDescriptionElements = productDescriptionElements.findChildren(
                "span", class_="a-list-item"
            )
    except:
        productDescriptionElements = []
    productDescription = ""
    for element in productDescriptionElements:
        productDescription += element.text + ", "
    return {
        "title": title,
        "price": price,
        "image": image,
        "description": productDescription,
    }
