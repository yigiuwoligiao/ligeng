import requests
import time
from lxml import etree
import random

requests.packages.urllib3.disable_warnings()

url = 'https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}
response = requests.get(url, headers=headers, verify=False)
html = response.text
print('状态码', response.status_code)

# 1) 抓取Best Sellers栏目下所有产品分类
html = etree.HTML(html)

# 链接
classify_url = html.xpath('//ul[@id="zg_browseRoot"]/ul/li/a/@href')
classify_url_list = []

for i in classify_url:
    classify_url_list.append(i)
print(len(classify_url_list))

# 2) 从1)中随机选取一个分类，抓取该分类下top100产品列表
url2 = random.choice(classify_url_list)
url2 = url2.rsplit('/', 2)[0]
# print('原本的url',url2)
url2 = url2 + '/ref=zg_bs_pg_2?_encoding=UTF8&pg='
# print('拼接的',url2)
shop_ls = []
for pg in range(1, 3):
    response = requests.get(url2 + str(pg), headers=headers, verify=False)
    # print('进入循环后的',url2)
    html = response.text
    html = etree.HTML(html)
    ls = html.xpath('//ol[@id="zg-ordered-list"]/li')
    # top100商品链接

    for i in ls:
        a_num = i.xpath('.//span[@class="zg-badge-text"]/text()')
        # print('序号', a_num)
        a_url = i.xpath('.//span[@class="aok-inline-block zg-item"]/a[1]/@href')
        # print('链接',a_url)
        shop_ls.append(a_url)

# 3) 从2)中随机选取一个产品，抓取该产品listing内容、评论、星级、售价等数据，也可自由发挥抓取其它数据。
# 要求： 引用python包请注明版本号，结果与实现代码请一并发送。
print(len(shop_ls))
detail_url = 'https://www.amazon.com' + random.choice(shop_ls)[0]
print('具体商品链接', detail_url)
response = requests.get(detail_url, headers=headers, verify=False)
html = etree.HTML(response.text)
title = html.xpath('//span[@id="productTitle"]/text()')

print('商品名', title)
price = html.xpath('//span[@id="priceblock_ourprice"]/text()')
print('价格', price)
pinglun_ls = html.xpath('//div[@class="a-section review-views celwidget"]/div')
for i in pinglun_ls:
    content = i.xpath(
        './/div[@class="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"]/span/text()')
    if len(content) > 0:
        content = content
        print(content)
    else:
        content = '当前没人评论'
        print(content)
    star = i.xpath('.//i[@class="a-icon a-icon-star a-star-5 review-rating"]/span/text()')
    print(star)
    print('=' * 200)
