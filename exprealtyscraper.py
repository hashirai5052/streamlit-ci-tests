import os
import time
import re
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import requests
from selenium.webdriver.common.keys import Keys
from random import randrange
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import logging

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)

# def setup_logging():
# logging.basicConfig(
# filename='app.log',           # Log file name
# level=logging.DEBUG,          # Logging level (can be adjusted based on needs)
# filemode='a',                 # Append to the file (do not overwrite)
# format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
# datefmt='%Y-%m-%d %H:%M:%S'    # Date format for the timestamp
# )


class DebugOnlyFilter(logging.Filter):
    def filter(self, record):
        # Allow only messages that are DEBUG level and from the "my_app" logger.
        # Change 'my_app' to the name of your logger if needed.
        return record.levelno == logging.DEBUG and record.name == "my_app"


def setup_logging():
    # Create your custom logger (instead of using the root logger)
    logger = logging.getLogger("my_app")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('app.log', mode='a')
    file_handler.setLevel(logging.DEBUG)

    # Attach the custom filter
    file_handler.addFilter(DebugOnlyFilter())

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    # Prevent propagation to the root logger so other handlers don't capture these logs
    logger.propagate = False

    return logger


logger = setup_logging()


def getsource():
    clist = ['US']  # ,'AL', 'AZ', 'KG', 'BA', 'UZ', 'BI', 'XK', 'DE', 'AT','UK', 'GB', 'IE', 'IM', 'FR', 'ES', 'NL', 'IT', 'PT', 'BE', 'AD', 'MC', 'MA', 'LU', 'DK', 'FI', 'NO', 'EU', 'VA']
    content = ''
    xdriver = ''
    try:
        chooseip = random.choice(clist)
        content = ''

        SBR_WEBDRIVER = 'https://brd-customer-hl_2aa4f566-zone-referal2haziq-country-' + \
            chooseip.lower()+':kilai54qoc5l@brd.superproxy.io:9515'
        # SBR_WEBDRIVER = 'https://brd-customer-hl_2aa4f566-zone-referal2haziq:kilai54qoc5l@brd.superproxy.io:9515'

        # SBR_WEBDRIVER= 'https://brd-customer-hl_2aa4f566-zone-scraping_browser_haziq-country-'+chooseip.lower()+':w08yu9g4ve6v@brd.superproxy.io:9222'
        # SBR_WEBDRIVER = f'wss://{AUTH}@brd.superproxy.io:9222'
        print(SBR_WEBDRIVER)

        sbr_connection = ChromiumRemoteConnection(
            SBR_WEBDRIVER, 'goog', "chrome")
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            checkip = 'https://geo.brdtest.com/mygeo.json'
            driver.get(checkip)
            # print('checking ip')
            # print(driver.page_source)

    except Exception as e:
        print(e)

      #  input(e)
        if 'ip_forbidden' in str(e).lower():
            content = str(e).strip()
            print("brightdata ad ip")

    return sbr_connection, content


def getdata(driver):
    email = phone = ''
    try:
        # driver.get_screenshot_as_file('mm5.png')
        # wait until page is loaded
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "body")))

        ct_elements = driver.find_elements(
            By.CLASS_NAME, "style_personal-contact__m9EXn")

        emailregex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phoneregex = r"(\(\d{3}\)\s*\d{3}[-.\s]?\d{4})"

        email, phone = None, None

        for ct in ct_elements:
            text = ct.text
            if not email:
                email_match = re.search(emailregex, text)
                if email_match:
                    email = email_match.group()

            if not phone:
                phone_match = re.search(phoneregex, text)
                if phone_match:
                    phone = phone_match.group()

            if email and phone:  # Stop if both are found
                break

        return email, phone

    except:
        capture_full_page_screenshots(driver, 'GETDATA_error')
        print('ERROR | GETDATA | 2')


def capture_full_page_screenshots(driver, agent_name, scroll_step=800):

    # Create a unique folder with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_name = f"screenshots_{agent_name}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    # Get total page height
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll to top before starting
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)

    # Start taking screenshots while scrolling
    scroll_position = 0
    screenshot_count = 1

    while scroll_position < total_height:
        # Generate unique filename
        letters = 'abcdefghijklmnopqrstuvwxyz'
        random_suffix = ''.join(random.choice(letters) for _ in range(5))
        screenshot_path = os.path.join(
            folder_name, f"error_{agent_name}_{screenshot_count}_{random_suffix}.png")

        # Take screenshot
        driver.save_screenshot(screenshot_path)

        # Scroll down
        scroll_position += scroll_step
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)  # Wait for page to load

        screenshot_count += 1

    print(f"All screenshots saved in: {folder_name}")


def fetch_data_sm(agent_name, driver):

    email = phone = link = ''
    found = False

    # Build the search query from agent_name
    parts = agent_name.split()
    if len(parts) > 2:
        search_query = f"{parts[0]}+{parts[-1]}"
    else:
        search_query = "+".join(parts[:2])
    url = f"https://www.exprealty.com/agents-search?page=1&country=US&name={search_query}"

    def attempt_extraction():
        # Click "Accept All" cookies if present
        try:
            accept_btn = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Accept All')]")
            accept_btn.click()
        except:
            pass

        time.sleep(10)
        # Try finding agent by image or by name link
        clicked = False
        try:
            img = driver.find_element(By.XPATH, f".//img[@alt='{agent_name}']")
            img.click()
            clicked = True
        except:
            try:
                name_link = driver.find_element(
                    By.XPATH, f".//a[contains(text(), '{agent_name}')]")
                name_link.click()
                clicked = True
            except:
                try:
                    # if name had 3 words, try the first and last name
                    if len(parts) > 2:
                        shortedName = f"{parts[0]}+{parts[-1]}"
                        name_link = driver.find_element(
                            By.XPATH, f".//a[contains(text(), '{shortedName}')]")
                        name_link.click()
                        clicked = True
                except:
                    # check if there's only one class with style_agent-card__h_hjj if yes, check if any of our agent name match that name, if yes click it.
                    try:
                        agent_card = driver.find_elements(
                            By.CLASS_NAME, "style_agent-card__h_hjj")
                        if len(agent_card) == 1:
                            agent_card[0].click()
                            clicked = True

                    except:
                        if not clicked:
                            print(f"Agent '{agent_name}' not found.")
                            capture_full_page_screenshots(driver, agent_name)
                            pass

        if not clicked:
            return '', '', ''  # Could not find/click agent
        print("clicked!")
        time.sleep(20)
        link_ = driver.current_url

        email_, phone_ = getdata(driver)
        return email_, phone_, link_

    # Try up to 3 times (1 load + 2 refreshes)
    for attempt in range(2):
        try:
            if attempt == 0:
                driver.get(url)
            else:
                driver.refresh()
                time.sleep(10)  # Wait after refresh
            # check if the page is loaded
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            if "We couldn’t find any matches for your search." in driver.page_source:
                print(f"Agent '{agent_name}' not on EXP.")
                break

            # Attempt to extract data
            email, phone, link = attempt_extraction()

            if email or phone:
                found = True
                break
            else:
                print(f"Attempt {attempt+1}: No data found.")
        except Exception as e:
            # If there's a big error, break and handle screenshot
            print(f"Error during attempt {attempt+1}: {e}")
            break

    # If not found after all attempts, do a screenshot for debugging
    if not found:
        try:
            print(f"Agent '{agent_name}' not found.")
            capture_full_page_screenshots(driver, agent_name)
            link = f'./datass/{agent_name}.png'
        except:
            pass

    return email, phone, link, found


def search_agent(agent_name):

    email = phone = link = ''
    found = False

    # We'll try up to 2 different connections (IPs)
    for attempt_ip in range(2):

        sbr_connection, content = getsource()
        if 'forbidden' in content.lower():
            print("IP is forbidden; trying the next IP.")
            continue

        # Configure the driver
        options = ChromeOptions()
        options.headless = True
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        print(
            f"Scraping info for '{agent_name}', IP attempt #{attempt_ip + 1}")
        try:
            with Remote(command_executor=sbr_connection, options=options) as driver:
                driver.set_window_size(1920, 1080)

                email_, phone_, link_, found_ = fetch_data_sm(
                    agent_name, driver)
                if found_:
                    email, phone, link, found = email_, phone_, link_, found_
                    break
        except Exception as e:
            print(f"Error with driver on IP attempt #{attempt_ip+1}: {e}")

    if not found:
        print(f"Agent '{agent_name}' not found or data not extracted.")

    return [email, phone]


searchlist = ['Alicia Lewis-Peele', 'Alicia Lewis-Peele',
              'Alicia Lewis-Peele', 'Alicia Lewis-Peele']

    # searchlist.delete(chooseagent)
    # time.sleep(60)
    # input('next')
# print(search_agent('Jennifer Hoyt'))
##
