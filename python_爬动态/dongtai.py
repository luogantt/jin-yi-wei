#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:31:26 2021

@author: ledi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:09:07 2021

@author: ledi
"""

import time
import parsel
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

url = 'http://www.neeq.com.cn/disclosure/supervise.html'

browser = webdriver.Chrome()

# wait = WebDriverWait(browser, 15)
time.sleep(5)

browser.get(url)

# wait = WebDriverWait(browser, 5)
time.sleep(5)
# time.sleep(3)

# url = 'http://www.xiniudata.com/investor/557fbd26fe9452145ef1160a37d347a1/overview'

# browser.get(url)

result=[]

for n in range(0,13):
    page = browser.page_source
    
    df=pd.read_html(page)
    result.append(df[0])
    # selector = parsel.Selector(page)

    # divs = selector.xpath('//*[@id="root"]/div[4]/div/div/div[1]/div/div[2]')

    # for div in divs:
    #     msg = div.xpath('.//text()').getall()
        
    #     print(msg)

    #     with open('红衫中国.txt', mode='a', encoding='utf-8', newline='')as f:
    #         csv_write = csv.writer(f)
    #         csv_write.writerow(msg)
        
    #     result.append(msg) 

    btn = browser.find_element_by_class_name('next')
    btn.click()
    time.sleep(1)



df1=pd.concat(result)

df1.to_csv('df1.csv',index=False)






