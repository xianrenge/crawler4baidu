#coding=utf-8

import urllib
import urllib.request as url
from urllib import parse
import re
from bs4 import BeautifulSoup as BS

pattern_link=re.compile(r'<h3 class="t">.*?href="(.*?)"',re.S)
pattern_next_page=re.compile(r'下一页',re.S)
pattern_front_page=re.compile(r'上一页',re.S)
pattern_page_num_first=re.compile(r'id="page">(.*?)</p>',re.S)

baseUrl = 'http://www.baidu.com/s'
page = 1 #第几页
word = '穿戴设备'  #搜索关键词

data = {'wd':word,'pn':str(page-1)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}
# data = urllib.urlencode(data)
data = parse.urlencode(data)
urll = baseUrl+'?'+data

try:
    request = url.Request(urll)
    response = url.urlopen(request)
    # print(response)
except:
    # print(e.code)
    print('error')
    exit(0)
# except urllib2.URLError,e:
#     print(e.reason)
#     exit(0)

html = response.read().decode("utf-8")
soup = BS(html)
td = soup.find_all(class_='f')
# print(td)
ps=soup.find_all(id='page')
# print(ps)
pss=ps[0].find_all('a')
links=[]
for p in pss:
    links.append(p.get('href'))
# print(list(set(links)))
print(len(list(set(links))))

# 提取出搜索结果的页数
def Get_Page_Num(pattern_page_num_first,page,front,next):
    aim=re.compile(r'href="(.*?)"',re.S)
    # item = re.findall(pattern_page_num_first, page.text)
    # print(page)
    item = re.findall(pattern_page_num_first, page)
    str=item[0]
    result=re.findall(aim,str)
    length=len(result)
    if(front==True) and (next==True):#多了一个链接
        length=length-1
    if(length==0):#只有一页
        length=1
    return length

print(Get_Page_Num(pattern_page_num_first,html,False,True))
# print(td)
cons=[]

def get_lists(td):
    for t in td:
        text={'title':'','url':'','realtime':'','content':''}
        # print(t.h3.a.get_text())
        # print(t.h3.a['href'])
        text['title']=t.h3.a.get_text().strip()
        text['url']=t.h3.a['href'].strip()

        font_str = t.find_all('font',attrs={'size':'-1'})[0].get_text()
        start = 0 #起始
        realtime = t.find_all('div',attrs={'class':'realtime'})
        if realtime:
            realtime_str = realtime[0].get_text()
            start = len(realtime_str)
            # print(realtime_str)
            text['realtime'] = realtime_str.strip()
        # else:


        end = font_str.find('...')
        # print(font_str[start:end+3],'\n')
        text['content'] = font_str[start:end+3].strip()
        # print(text)
        if text not in cons:
            cons.append(text)

get_lists(td)
links=list(set(links))
for lk in links:
    url0='http://www.baidu.com/'+lk
    try:
        request = url.Request(url0)
        response = url.urlopen(request)
    except:
        # print(e.code)
        print('error')
        exit(0)
    html = response.read().decode("utf-8")
    soup = BS(html)
    td = soup.find_all(class_='f')
    get_lists(td)
print(cons)
print(len(cons))