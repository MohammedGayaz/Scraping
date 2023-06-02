import requests
import csv
import time
from bs4 import BeautifulSoup


HEADER_DATA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
URL = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
FILE = 'product_list.csv'

headers = {'User-Agent': HEADER_DATA}
source = requests.get(URL, headers=headers).text
soup = BeautifulSoup(source, 'lxml')


# Seller name for each product
def get_seller_data(links):
    seller = []
    for j in range(len(links)):
        a = True
        while a:
            try:
                time.sleep(7)
                headers = {'User-Agent': HEADER_DATA}
                source = requests.get(links[j], headers=headers).text
                soup = BeautifulSoup(source, 'lxml')
                i = soup.find("div", attrs={"id": 'merchant-info'})
                yString = i.text
                seller.append(yString)
                a = False

            except AttributeError:
                pass

    return seller


# rating of the product
def get_rating_data():
    rating = []
    for i in soup.find_all('span', class_='a-icon-alt'):
        rating.append(i.text)

    return rating


# getting price of the product
def get_price_data():
    price = []
    for i in soup.find_all('span', class_='a-price-whole'):
        price.append(i.text)

    return price


# getting name of the product
def get_name_data():
    name = []
    for i in soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal'):
        name_str = i.text
        name.append(name_str.strip())

    return name


# getting link of all products
def get_link_data():
    links = []
    for i in soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
        links.append("https://www.amazon.in/" + i["href"])

    return links


# writing data to file
def write_file(name, price, rating, seller):
    with open(FILE, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['S.No', 'Name', 'Prices', 'Rating', 'Seller'])
        for i in range(len(name)):
            writer.writerow([i+1, name[i], price[i], rating[i], seller[i]])


print("scraping started")

product_links = get_link_data()
# print(product_links)

product_names = get_name_data()
# print(product_names)

product_prices = get_price_data()
# print(product_prices)

product_ratings = get_rating_data()
# print(product_ratings)

product_sellers = get_seller_data(product_links)
# print(product_sellers)

write_file(product_names, product_prices, product_ratings, product_sellers)
print("scraping endec")
