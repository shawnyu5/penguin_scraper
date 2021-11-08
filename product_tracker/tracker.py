# !/usr/bin/env python3
# purpose of this file:
# Date: 2021-10-13
# ---------------------------------
import sys
from bs4 import BeautifulSoup
import requests
import json
sys.path.insert(1, '/home/shawn/python/web_scraping/penguin_bots/') # utils
import utils  # type: ignore

def to_object(title:str, discount:str, price:str):
    return {
            "title": title,
            "discount_percent": discount,
            "price": price,
            "appearances": 1 # going to assume first appearance until other wise
            }

def validate(product) -> bool:

    with open("/home/shawn/python/web_scraping/penguin_bots/product_tracker/current_product.json", "r") as file:
        file_product = json.load(file)

    with open("/home/shawn/python/web_scraping/penguin_bots/product_tracker/current_product.json", "w") as file:
        json.dump(product, file, indent=4)

    if file_product["title"] == product["title"]:
        return False
    else:
        return True

# return in the index which the search term appears in the array. -1 if nothing is found
def index(array, search_term) -> int:
    index = 0
    for current in array:
        if current["title"] == search_term["title"]:
            return index
        index = index + 1
    return -1

# add the current product to
def to_file(current_product):
    with open("/home/shawn/python/web_scraping/penguin_bots/product_tracker/products.json", "r+") as file:
        product_arr = json.load(file)

        # checks if current product is logged and return the index.
        found_index = index(product_arr, current_product)

        # if product is logged, remove the product from list
        if found_index != -1:
            removed_product = product_arr.pop(found_index)

            # not all products saved has a appearance attribute
            if "appearances" not in removed_product:
                current_product["appearances"] = 2
            else:
                current_product["appearances"] = removed_product["appearances"] + 1
                current_product["price"] =  current_product["price"] / current_product["appearances"]

        product_arr.append(current_product)

        print("product saved:", current_product)

    with open("/home/shawn/python/web_scraping/penguin_bots/product_tracker/products.json", "w+") as file:
        json.dump(product_arr, file, indent=4)


def main():
    url = "https://www.penguinmagic.com/openbox"

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, "html.parser")

    product_title = utils.get_title(soup)
    product_discount_percentage = utils.get_discount_percentage(soup)
    product_discount_price = utils.get_discounted_price(soup)

    product = to_object(product_title, product_discount_percentage, product_discount_price) #type: ignore

    # if product has not changed, save product to file and don't parse json
    # file
    if not validate(product):
        print("Product has not changed")
        print(product)
        exit(0)

    to_file(product)


if __name__ == "__main__":
    main()

