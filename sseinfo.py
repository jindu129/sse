import requests 
from bs4 import BeautifulSoup
import os

session = requests.session()

try:
    url = 'https://www.sseinfo.com/services/assortment/document/'
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               # 防盗链，溯源，当前请求的上一级是https://www.sseinfo.com/
               "Refer": "https://www.sseinfo.com/"}
    resp = requests.get(url, headers=headers)
    #print('检查resp:',resp)
    #print('打印头信息:', resp.headers)
    #print('第一次打印html:', resp.text)
    resp.encoding = "utf-8"
    #print('第二次打印html:', resp.text)
    
    
    #解析数据
    #1. 把页面源代码交给BeautifulSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")
    #print('打印BeautifulSoup解析的bs对象', page)
    
    # 2. 从bs对象中查找数据
    # find（标签，属性=值）
    # find_all（标签，属性=值）
    s = page.find("div", class_="row-one") #class_，class后加下划线是为了区分class关键字
    #print(s)
    alist = page.find("div", class_="row-one").find_all("a")
    #print(alist)
    
    # 3. 通过href拿到自页面的内容，从自页面中找到pdf的下载地址
    #[['/services/assortment/document/interface/c/5705501.pdf', '上海证券交易所LDDS系统新加坡交易所行情接口说明书(1.0.1)_20220708'], [], ...[]]
    urls = []
    for a in alist:
        href = a.get('href')
        urls.append(str(href))
        #child_page_resp = requests.get('https://www.sseinfo.com/' + 'href')
        print(a.get('href')) #直接通过get就可以拿到属性的值
        print(a.get('title')) #直接通过get就可以拿到属性的值
    #print(urls)
    
    for url in urls:
        try:
            url = 'https://www.sseinfo.com' + url
            resp = session.head(url, allow_redirects=True)
            resp.raise_for_status()
            if resp.headers['content-type'] == 'application/pdf':
                resp = session.get(url)
                if resp.ok:
                    with open(os.path.basename(url), 'wb') as outfile:‘wb’: #表示以二进制写方式打开,只能写文件, 如果文件不存在,创建该文件;如果文件已存在,则覆盖写。
                        outfile.write(resp.content)
                        print ("Saved {} to file {}".format(url, os.path.basename(url)))
                else:
                    print ('GET request for URL {} failed with HTTP status "{} {}"'.format(url, resp.status_code, resp.reason))
        except requests.HTTPError as exc:
            print("HEAD failed for URL {} : {}".format(url, exc))   
    
except requests.HTTPError as exc:
    print ("HEAD failed for URL {} : {}".format(url, exc))
