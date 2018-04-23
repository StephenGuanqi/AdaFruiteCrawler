import requests
from bs4 import BeautifulSoup
import re
from time import time
import sys


def get_categories_list():
    """
    get all "More" button urls from the categories website
    :return:  a list of urls
    """
    url = "https://www.adafruit.com/categories"
    response = requests.get(url)
    if response.status_code != 200:
        print("retrieve categories main web site failed")
        return []

    urls = []
    categories = []

    soup = BeautifulSoup(response.text, "html.parser")

    # parse all categories and relative urls
    main_container = soup.find('div', class_='main-container container')
    categories_tags = main_container.find_all('div', class_='col-lg-11 col-md-11 col-sm-11 col-xs-11')
    top_twenties = main_container.find_all('div', class_="row top-twenty")

    for category in categories_tags:
        categories.append(category.h3.a.string)

    for top_twenty in top_twenties:
        a = top_twenty.div.div.a
        urls.append("https://www.adafruit.com/" + a.get('href'))

    return categories, urls


def get_all_item_tags(url):
    """
    parse all items' tags from specific category url and get the all items tag
    :param url: specific categories' url
    :return: item tags
    """
    response = requests.get(url)
    if response.status_code != 200:
        print("retrieve categories items failed")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    item_tags = soup.find_all('div', class_="row product-listing")
    return item_tags


def parse_item_tag(item_tag, category):
    """
    Parse all attributes of the tag and then convert them to dictionary
    :param item_tag: input html tag objects
    :param category: category of this item
    :return: a dictionary contains all attributes of the projects
    """
    image_tag = item_tag.find_all('div')[0]
    info_wrapper = item_tag.find('div', class_='product-listing-text-wrapper')
    info = item_tag.find('div', class_='product-info clearfix row')

    # check on availability first
    availability_tag = info.find('div', class_='stock')
    if not availability_tag or not availability_tag.span or not availability_tag.span.string:
        return None
    availability = availability_tag.span.string

    # if the item's status is IN STOCK, don't continue parsing and return
    if availability.strip() == 'OUT OF STOCK':
        item = {'Availability': 'OUT OF STOCK', 'Amount': 0}
    else:
        m = re.search("(\d+) IN STOCK", availability.strip())
        if not m:
            return None
        item = {'Availability': 'IN STOCK', 'Amount': float(m.group(1))}

    item["image_url"] = image_tag.a.img.get('src')
    item["name"] = info_wrapper.h1.a.string.strip()
    item["url"] = "https://www.adafruit.com" + info_wrapper.h1.a.get('href')
    item["ID"] = info_wrapper.find('div', class_="product_id").span.string
    item["description"] = info_wrapper.find('div', class_="product-description clearfix hidden-sm hidden-xs hidden-md").string.strip()
    item["category"] = category

    price_tag = info.find('span', class_="normal-price")
    if not price_tag.span and price_tag.string is not None:
        item["price"] = float(re.findall("\d+\.\d+", price_tag.string)[0].replace(',',''))
    elif price_tag.span.string is not None:
        item["price"] = float(price_tag.span.string.replace(',',''))
    # print(item)
    return item


# single thread parsing test
if __name__ == '__main__':
    ts = time()
    categories, urls = get_categories_list()
    print(categories)
    print(urls)
    print(len(urls)) # 34
    print('Took {}s to parse urls'.format(time() - ts))  # 7.5 s

    category_tags = []
    ts = time()
    for category, url in zip(categories, urls):
        item_tags = get_all_item_tags(url)
        category_tags.extend([(category, tag) for tag in item_tags])
    print(sys.getsizeof(category_tags))  # 44KB
    print('Took {}s to parse all tags'.format(time() - ts))  # 72 s
    print(len(category_tags))  # 4936

    items = []
    ts = time()
    for category, tag in category_tags:
        item = parse_item_tag(tag, category)
        if not item:
            continue
        items.append(item)
    print(sys.getsizeof(items)) # 14 kb
    print('Took {}s to parse all items'.format(time() - ts)) # 3.4 s
    print(len(items))  # 1742