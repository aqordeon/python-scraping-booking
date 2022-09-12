import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable
import time



class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_curreny(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR,
            'button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        selected_currency_element = self.find_element(By.CSS_SELECTOR,
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID,
            'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_option = self.find_element(By.CSS_SELECTOR,
            'li[data-i="0"]')
        first_option.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR,
                                              f'td[data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_element = self.find_element(By.CSS_SELECTOR,
                                              f'td[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adult(self, count=1):
        select_adult_element = self.find_element(By.ID, 'xp__guests__toggle')
        select_adult_element.click()

        while True:
            adult_decrease_element = self.find_element(By.CSS_SELECTOR,
                                                       'button[aria-label="Decrease number of Adults"]')
            adult_value_element = self.find_element(By.ID, 'group_adults').get_attribute('value')
            adult_decrease_element.click()
            if int(adult_value_element) == 1:
                break

        for _ in range (count-1):
            adult_increase_element = self.find_element(By.CSS_SELECTOR,
                                                       'button[aria-label="Increase number of Adults"]')
            adult_increase_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR,
                                          'button[type="submit"')
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(5)
        time.sleep(3)
        filtration.sort_price_lowest_first()

    def report_results(self):
        report = BookingReport(html_doc=self.current_url)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Score"])
        table.add_rows(report.pull_hotel_data())
        print(table)
