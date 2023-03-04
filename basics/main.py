import logging
import re
import sys
import time
from platform import system
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


if system() != "Windows":
    logging.error("Avaiable only at Windows!")
    sys.exit(0)


def log(message: str) -> None:
    """
    create a log
    :param message: message to create log
    :return:
    """
    logging.basicConfig(filename="selenium_basic_bot.log",
                        format='%(asctime)s::%(levelname)s:: %(message)s',
                        filemode='w',
                        level=logging.INFO)
    logging.info(message)


def check_url_pattern(url: str) -> bool:
    base = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&" \
           "\\/=]*)$"
    try:
        if isinstance(re.match(base, url).group(0), str):
            return True
    except AttributeError:
        return False


def open_navigator() -> WebDriver:
    global options
    driver = webdriver.Chrome(executable_path='../driver/chromedriver.exe', options=options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(8)
    log("Open Chrome successfully")
    return driver


def close_navigator(driver: WebDriver):
    driver.close()
    log("Finished")
    sys.exit(0)


def wait_until_element_appear(driver: WebDriver, element: str) -> None:
    """
    :param driver: WebDriver
    :param element: "Download",etc
    :return:
    """
    WebDriverWait(driver, 30).until(
        expected_conditions.text_to_be_present_in_element(
            (By.CLASS_NAME, 'menu-cta'),  # Element filtration
            element  # Expected text
        )
    )


def http_request(url: str) -> None:
    """
    send request to choised website
    :param url: url to make automation
    :return:
    """
    assert check_url_pattern(url), "INVALID URL"
    driver = open_navigator()
    driver.get(url)
    log(f"GET URL: {url}")
    find_elements(driver)


def find_elements(driver: WebDriver) -> None:
    """
    find specificated element
    :param driver: driver post http request
    :return:
    """
    log("looking for elements...")
    wait_until_element_appear(driver, "Download")
    download_button = driver.find_element(by=By.CLASS_NAME, value="menu-cta")
    log(f"Download button identify: {download_button.text}")
    close_navigator(driver)


if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("detach", True)
    http_request("https://www.princexml.com/samples/")
