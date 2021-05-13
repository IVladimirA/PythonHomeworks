import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    table = parser.body.center.table
    rows = []
    for row in table.findAll("tr"):
        rows.append(row)
    content = rows[3].findAll("tr")
    for i in range(0, len(content) - 2, 3):
        page = dict()
        links = content[i + 1].findAll("td")[1].findAll("a")
        if len(links) < 4:
            continue
        page["points"] = int(content[i + 1].findAll("td")[1].span.text.split()[0])
        page["author"] = links[0].text
        comments = "discuss"
        if len(links) == 4:
            comments = links[3].text.split()[0]
        if comments == "discuss":
            page["comments"] = 0
        else:
            page["comments"] = int(comments)
        link = content[i].findAll("td")[2].find("a")
        page["url"] = link["href"]
        page["title"] = link.text
        news_list.append(page)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    table = parser.body.center.table
    rows = []
    for row in table.findAll("tr"):
        rows.append(row)
    content = rows[3].findAll("tr")
    print(len(content))
    if len(content) < 92:
        return "newest"
    page = content[-1].findAll("td")[1]
    return page.find("a")["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


# test = get_news("https://news.ycombinator.com", 2)
# print(test[35], "\n", test[5])
