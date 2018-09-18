#momo爬 L1類別
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse
def get_L1_dict():
    url = "https://www.momomall.com.tw/main/Main.jsp"
    UA ='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
    header = { "User-Agent" : UA,
               }
    res = requests.get(url, headers = header)
    bsObj = BeautifulSoup(res.text,'html.parser')
    pat = re.compile('/m/s/category/(\d+)/(.+)')
    L1_list = []
    for i in bsObj.findAll('a',{'class':'lookAll'}):
        s = re.search(pat,i['href'])
        L1 = {s.group(1) : s.group(2)}
        L1_list.append(L1)
    return L1_list
def get_L2_dict(L1_code):
    #l2類別
    UA ='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
    url = "https://www.momomall.com.tw/category/LCategory.jsp"
    data = {'category_code': L1_code,#L2
    'doAction': 'getCategoryTreeList'}#getCategoryList可以找到下兩個類別 getCategoryTreeList只能找到子類別
    header = { "User-Agent" : UA,
               }
    res_list = requests.post(url,data = data, headers = header)
    res_list.encoding = 'utf8'
    L2_dict = {}
    for i in json.loads(res_list.text)['cateTree'][1:]:
        L2_dict[i['CATEGORY_CODE']] = i['CATEGORY_NAME']
    return L2_dict  
def get_L3_dict(L2_code):
    #l2類別
    UA ='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
    url = "https://www.momomall.com.tw/category/LCategory.jsp"
    data = {'category_code': L2_code,#L2
    'doAction': 'getCategoryTreeList'}
    header = { "User-Agent" : UA,
               }
    res_list = requests.post(url,data = data, headers = header)
    res_list.encoding = 'utf8'
    L3_dict = {}
    for i in json.loads(res_list.text)['cateTree'][1:]:
        L3_dict[i['CATEGORY_CODE']] = i['CATEGORY_NAME']
    return L3_dict
def get_L4_dict(L3_code):
    #l2類別
    UA ='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
    url = "https://www.momomall.com.tw/category/LCategory.jsp"
    data = {'category_code': L3_code,#L3
    'doAction': 'getCategoryTreeList'}
    header = { "User-Agent" : UA,
               }
    res_list = requests.post(url,data = data, headers = header)
    res_list.encoding = 'utf8'
    L4_dict = {}
    for i in json.loads(res_list.text)['cateTree'][1:]:
        L4_dict[i['CATEGORY_CODE']] = i['CATEGORY_NAME']
    return L4_dict
def get_page_url(L4_code, L4_cat_name,page,order=4):
    #get single page item url
    url = "https://www.momomall.com.tw/s/category/"+L4_code+"/"+str(order)+"/"+str(page)+"/"+urllib.parse.quote(L4_cat_name)
    #https://www.momomall.com.tw/s/category/2000100353/4/2/%E5%BE%8C%E8%83%8C%E5%8C%85
    UA ='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
    header = {"User-Agent" : UA}
    #page: 1, orderby: 4 >銷量排行
    res = requests.get(url, headers = header)
    bsObj = BeautifulSoup(res.text,'html.parser')
    if bsObj.select('#surveyContent')[0].findAll('li') != []:
        for i in bsObj.select('#surveyContent')[0].findAll('li'):
            print('https://www.momomall.com.tw'+i.a['href'][2:])
    else:
        print('查無結果')
        return None