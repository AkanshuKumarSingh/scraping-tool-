"""
Module for defining Scrapper class and its implementation
"""


import os
import json
import time

import requests
from bs4 import BeautifulSoup
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


class Scraper:
    """
    Class to scrap elements from website.
    """
    

    def __init__(self, data: dict, retry_sec: int = 5, max_retries: int = 5) -> None:
        """
        Constructor method to initialize the required variables
        
        Args:
            data(Dict): dict containing the request data to be used for processing.
            retry_sec(int): retry timing
            max_retries(int): max retries
        """
        
        self.base_url = "https://dentalstall.com/shop/page/{}/"
        self.config = data
        self.product_selected = []
        self.retry_sec = retry_sec
        self.max_retries = max_retries

    def fetch_page_data(self, page_number: int) -> str:
        """
        Method to fetch page data from required url.

        Args:
            page_number(int): Page Number from which we will fetch the data.
        
        Returns:
            str: string containing HTML data.
        """
        
        for retry in range(0, self.max_retries):
            try:
                response = requests.get(
                    self.base_url.format(page_number), 
                    proxies={"http": self.config.proxy, "https": self.config.proxy} if self.config.proxy else None
                )
                response.raise_for_status()
                return response.text
            except Exception as exp:
                if retry == self.max_retries-1:
                    raise exp
                time.sleep(self.retry_sec)

    def parse_page(self, html_content: str) -> None:
        """
        Method to filter required data from html content.

        Args:
            html_content: html data.
        
        Returns:
            None
        """
        
        soup_obj = BeautifulSoup(html_content, 'html.parser')
        product_cards = soup_obj.find_all('div', class_='product-inner')

        for card in product_cards:
            title = card.find('h2', class_='woo-loop-product__title').get_text(strip=True)
            price = card.find('bdi').get_text(strip=True)
            image = card.find('img', class_='attachment-woocommerce_thumbnail')['data-lazy-src']

            cached_price = redis_client.hget(title, "price")
            if cached_price and cached_price == price:
                print(f"Skipping {title}: Price has not changed.")
                continue

            redis_client.hset(title, mapping={"price": price, "image": image})

            self.product_selected.append({
                "product_title": title,
                "product_price": price,
                "path_to_image": self.process_image(image, title)
            })

    def process_image(self, image_url: str, product_name: str) -> str:
        """
        Method to dowload image and save to folder locally.

        Args:
            image_url: image url.
            product_name: name of product.
        
        Returns:
            None
        """

        response = requests.get(image_url)
        response.raise_for_status()

        image_name = f"{product_name.replace(' ', '_')}.jpg"
        image_path = os.path.join("images", image_name)
        os.makedirs("images", exist_ok=True)

        with open(image_path, "wb") as file:
            file.write(response.content)

        return image_path

    def notify(self) -> None:
        """
        Notify the users.        
        """
        
        print(f"Scraping process finished and {len(self.product_selected)} products scraped and saved to DB.")

    def start(self) -> None:
        """
        Method to start execution of scraping data from website.
        """
        
        page = 1
        while page <= self.config.max_pages:
            try:
                html_content = self.fetch_page_data(page)
                self.parse_page(html_content)
            except Exception as exp:
                print(f"Error scraping page {page}: {exp}")
                break
            
            page += 1

        
        # Save data to JSON
        with open("product_data.json", "w") as file:
            json.dump(self.product_selected, file)

        self.notify()
