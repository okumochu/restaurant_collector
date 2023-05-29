from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_comments(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)
    restaurant_name = driver.find_element(
        By.CLASS_NAME, 'DUwDvf.fontHeadlineLarge').text

    button = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]')))
    button.click()

    # scrolling
    time.sleep(2)
    result = driver.find_element(By.CLASS_NAME, 'jANrlb').find_element(
        By.CLASS_NAME, 'fontBodySmall').text
    result = result.replace(',', '')
    result = result.split(' ')
    result = result[0].split('\n')

    counter = min(int(int(result[0])/10), 4)

    # print(counter)
    time.sleep(10)
    for _ in range(counter):
        print('scrolling...')
        scrollable_div = driver.find_element(
            By.ID, "QA0Szd")
        scrolling = driver.execute_script(
            'document.getElementsByClassName("dS8AEf")[0].scrollTop = document.getElementsByClassName("dS8AEf")[0].scrollHeight', scrollable_div)
        time.sleep(3)
    print('finished scrolling')

    # get data
    time.sleep(15)
    print('get data...')
    more_elemets = driver.find_elements(By.CLASS_NAME, 'w8nwRe.kyuRq')
    for list_more_element in more_elemets:
        list_more_element.click()
    elements = driver.find_elements(By.CLASS_NAME, 'jftiEf')
    lst_data = []
    for data in elements:
        try:
            text = data.find_element(By.CLASS_NAME, 'wiI7pd').text
            lst_data.append(text)
        except:
            pass

    for i in range(len(lst_data)):
        lst_data[i] = lst_data[i].replace('\n', '')

    print(f'number of comments:{len(lst_data)}')

    time.sleep(10)
    driver.quit()
    return lst_data, restaurant_name
