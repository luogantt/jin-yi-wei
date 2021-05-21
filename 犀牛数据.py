import time
import parsel
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://www.xiniudata.com/'

browser = webdriver.Chrome()

wait = WebDriverWait(browser, 15)

browser.get(url)

time.sleep(3)

url = 'http://www.xiniudata.com/investor/557fbd26fe9452145ef1160a37d347a1/overview'

browser.get(url)

result = []

for n in range(0,30):
    page = browser.page_source
    selector = parsel.Selector(page)

    divs = selector.xpath('//div[@id="project-lib-table"]//div[contains(@class,"table-section")]')

    for div in divs:
        msg = div.xpath('.//text()').getall()

        with open('红衫中国.txt', mode='a', encoding='utf-8', newline='')as f:
            csv_write = csv.writer(f)
            csv_write.writerow(msg)
        
        result.append(msg) 

    btn = browser.find_element_by_xpath('//li[@class="next"]/a')
    btn.click()
    time.sleep(2)
