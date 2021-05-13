#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 18:44:42 2021

@author: ledi
"""

# from selenium import webdriver
# import time
# driver=webdriver.Chrome()
# url1='https://www.jisilu.cn/data/cbnew/#cb'
# bes=driver.get(url1)
# time.sleep(5)  #增加延时命令，等待元素加载
# driver.find_element_by_tag_name("tr").click()  #增加延时，等待元素加载
# table_tr_list=driver.find_element_by_xpath("//*[@id='flex_cb']").find_elements_by_tag_name("tr") #后面一个element改成elements
# for tr in table_tr_list:
#     if len(tr.get_attribute('id'))>0:
#         print(tr.find_element_by_xpath("//*[@id=%d]/td[1]/a"%(int(tr.get_attribute('id')))).text+" "+tr.find_element_by_xpath("//*[@id=%d]/td[2]"%(int(tr.get_attribute('id')))).text)
# # driver.quit()


# # https://www.hurun.net/zh-CN/Rank/HsRankDetailsList?num=IH8GTUI9&search

# # https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t
import requests
import json


# url='https://www.hurun.net/zh-CN/Rank/HsRankDetailsList?num=IH8GTUI9&search'
# return_data = requests.get(url,verify = False)
# js=return_data.json()
# for i in js['rows']:
#     print(i)
#     # print(i['id']+" "+i['cell']['bond_nm']+" "+i['cell']['price'])
    


url='https://www.hurun.net/zh-CN/Rank/HsRankDetailsList?num=IH8GTUI9&search'
return_data = requests.get(url,verify = False)
js=return_data.json()

cc=[]
for i in js:
    
    print(i)
    
    person=i['hs_Character'][0]

    cc.append([
               person['hs_Character_BirthPlace_Cn'],
               person['hs_Character_Permanent_Cn'],
               person['hs_Character_Education_Cn'],
               person['hs_Character_School_Cn'],
               i['hs_Rank_Global_Relations'],
               i['hs_Rank_Global_Ranking'],
               i['hs_Rank_Global_Wealth'],
               i['hs_Rank_Global_ChaName_Cn'],
               i['hs_Rank_Global_ComName_Cn'],
               i['hs_Rank_Global_Industry_En'],
               person['hs_Character_Age'],
               i['hs_Rank_Global_Industry_Cn']
               ])
import pandas as pd
vv=['出生地','常住地','学历','学校','关系','排名','财富','姓名','公司','行业','年龄','中文行业']
cc1=pd.DataFrame(cc,columns=vv)

cc1=cc1.replace({'未知': 100})
cc1['年龄']=cc1['年龄'].astype(int)
# cc1.replace('')
    # print(i['id']+" "+i['cell']['bond_nm']+" "+i['cell']['price'])




def show_analysis(year=40):
    # year=50
    cc2=cc1[cc1['年龄']<year]
    #显示所有列
    pd.set_option('display.max_columns', None)
    #显示所有行
    pd.set_option('display.max_rows', None)
    #设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth',100)
    
    cc3=cc2.sort_values(by='年龄')
    cc3.to_csv('青年富豪.csv',index=False)
    
    
    from collections import Counter
    
    c4=pd.Series(Counter(cc3['中文行业']))
    
    
    c5=c4.sort_values(ascending=False)
    
    c6=c5.iloc[:20]
    
    
    
    
    
    
    
    import matplotlib as mpl
    from matplotlib import pyplot as plt
    mpl.rcParams[u'font.sans-serif'] = ['simhei']
    mpl.rcParams['axes.unicode_minus'] = False
    
    
    x_data =list(c6.index)
    y_data =list(c6.values)
    
    #设置画布的尺寸
    plt.figure(figsize=(60,40))
    
    plt.bar(x_data,
            y_data,
            color=['b','r','g','y','c','m','y','k','c','g','g'],#颜色
            alpha=0.5,  # 透明度
            width=0.5,   # 每个条形的宽度
            edgecolor='red',  # 边框颜色
            linewidth=3  # 边框宽度
            )
    #柱状图上显示具体数据
    for a, b, label in zip(x_data, y_data,y_data):
        plt.text(a,
                 b,
                 label,
                 ha='center', 
                 va='bottom')
    #图例展示位置，数字代表第几象限
    
    # plt.title('Masked line demo')
    plt.title(str(year)+'岁以下富豪')
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.legend(loc=2)
    plt.savefig(str(year)+'.png')
    
    plt.show()

show_analysis(year=40)
show_analysis(50)















