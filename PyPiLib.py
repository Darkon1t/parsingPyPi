import requests
from bs4 import BeautifulSoup
import csv

URL = "https://pypi.org/search/?q=&o=&c=Programming+Language+%3A%3A+Python+%3A%3A+3"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/88.0.4324.190 Safari/537.36", "accept": "*/*"}


def get_html(url, params=None):
    data = requests.get(url, headers=HEADERS, params=params)
    return data


# Take home-page link about project

# def get_homepage(url):
#     data = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(data.text, "html.parser")
#     if soup.find("a", class_="vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed"):
#         output_info = soup.find("a", class_="vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--"
#                                             "condensed").get("href")
#     else:
#         return []
#     return output_info


def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("a", class_="button button-group__button")[:-1]
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="package-snippet")
    modules = []
    for item in items:
        info = item.find("p", class_="package-snippet__description").get_text(strip=True)
        if not info or type(info) is not str:
            info = "Information not found"
        modules.append({
            "name": item.find("span", class_="package-snippet__name").get_text(strip=True),
            "link": 'https://pypi.org/' + item.get("href"),
            "info": info,
            "version": item.find("span", class_="package-snippet__version").get_text(strip=True)
        })
    return modules


def save_file(items, path):
    with open(path, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["module", "link", "info", "version"])
        for item in items:
            writer.writerow([item["name"], item["link"], item["info"], f" {item['version']}"])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        modules = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            html = get_html(URL, params={"page": page})
            modules.extend(get_content(html.text))
        save_file(modules, "modules.csv")
    else:
        return "error"


parse()
