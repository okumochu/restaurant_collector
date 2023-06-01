from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_restaurant_urls(n_restaurants):
    # ignore the warnings and errors
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    url = "http://www.google.com/maps"
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(url)
    time.sleep(5)

    # search for the location
    location = input("請輸入所在地址，越詳細越好:")
    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(location)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    try:
        target = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
        )
        location_url = target.get_attribute("href")
        driver.get(location_url)
        time.sleep(5)
    except:
        pass

    # search restaurants by button

    try:
        button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="assistive-chips"]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/button',
                )
            )
        )
    except:
        button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="omnibox-singlebox"]/div[1]/div[4]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/button',
                )
            )
        )
    button.click()

    # search restaurants by search box

    # search_box = WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.NAME, "q"))
    # //input[@name='q']
    # )
    # search_box.clear()
    # search_box.send_keys("餐廳")
    # search_box.send_keys(Keys.ENTER)

    time.sleep(5)

    # scroll

    for i in range(n_restaurants // 5):
        scrollable_div = driver.find_element(
            By.CLASS_NAME,
            "lXJj5c.Hk4XGb",
        )
        scrolling = driver.execute_script(
            'document.getElementsByClassName("dS8AEf")[1].scrollTop = document.getElementsByClassName("dS8AEf")[1].scrollHeight',
            scrollable_div,
        )
        time.sleep(2)

    # get restaurant urls used to search

    time.sleep(5)
    elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    lst_url = []
    for i in range(n_restaurants):
        lst_url.append(elements[i].get_attribute("href"))

    return lst_url
