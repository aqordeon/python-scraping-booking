# This file is going to include methods that will parse
# The specific data that we need from each one of the deal box
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


class BookingReport:
    def __init__(self, html_doc:None):
        self.html_doc = html_doc

    def pull_hotel_data(self):
        html_text = requests.get(self.html_doc).content
        soup = BeautifulSoup(html_text, 'html.parser')
        all_hotel_box = soup.find_all(attrs={"data-testid": "property-card"})
        collection = []
        for hotel_box in all_hotel_box:
            hotel_score = hotel_box.select_one('div[data-testid="review-score"] div').get_text(strip=True)
            hotel_name = hotel_box.select_one('div[data-testid="title"]').get_text(strip=True)
            collection.append([hotel_name, hotel_score])

        return collection
