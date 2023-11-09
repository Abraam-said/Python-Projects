
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))

curr_page = 1
data = []

while True:

    print(curr_page)

    url = f'https://diwanegypt.com/product-category/books/arabic-books/page/{curr_page}/'
    driver.get(url)

    time.sleep(5)   # added a 5 seconds sleep

    books_links = driver.find_elements(
        By.XPATH, '//a[contains(@class, "woocommerce-LoopProduct-link woocommerce-loop-product__link")]')

    books_title = driver.find_elements(
        By.XPATH, '//h2[contains(@class, "woocommerce-loop-product__title")]')

    books_author = driver.find_elements(
        By.XPATH, '//span[contains(@class, "author")]')

    books_prices = driver.find_elements(
        By.XPATH, '//span[contains(@class, "price")]')

    books_img_urls = driver.find_elements(
        By.XPATH, '//img[contains(@class, "attachment-woocommerce_thumbnail ")]')

    last_page = driver.find_elements(
        By.XPATH, '//a[contains(@class, "page-numbers")]')

    if last_page:
        last_page = int(last_page[-2].text)
    else:
        last_page = curr_page

    for i in range(len(books_links)):
        try:
            book_links = books_links[i].get_attribute('href')
            book_title = books_title[i].text
            book_author = books_author[i].text
            book_prices = books_prices[i].text
            book_img_urls = books_img_urls[i].get_attribute('src')
            data.append([book_links, book_title, book_author,
                        book_prices, book_img_urls])
        except:
            pass

    if curr_page == last_page:
        break

    curr_page += 1

with open('data.csv', 'w', encoding='UTF-8') as fid:
    writer = csv.writer(fid)
    writer.writerow(['book_links', 'book_title', 'book_author',
                    'book_prices', 'book_img_urls'])
    writer.writerows(data)

driver.close()
