def extract_reviews(data):
    reviews = []
    container = data.findChild("div", class_="a-section review-views celwidget")
    try:
        elements = container.findChildren("div", class_="a-section review aok-relative")
    except:
        return []
    for element in elements:
        reviewerName = element.find("span", class_="a-profile-name").text
        rating = element.find("span", class_="a-icon-alt").text

        review = (
            element.findChild(
                "div",
                class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content",
            )
            .findChild("span")
            .text
        )
        reviews.append(
            {
                "reviewerName": reviewerName,
                "rating": rating,
                "review": review,
            }
        )
    return reviews
