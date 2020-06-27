# 案例：京东大药房爬虫
# https: // mall.jd.com / index - 1000015441.
# https://mall.jd.com/index-1000015441.html?cu=true&utm_source=baidu-search&utm_medium=cpc&utm_campaign=t_262767352_baidusearch&utm_term=113098950926_0_f4806f9c0e2e48bab760aa196dddf56c
# 爬取标题，价格，品牌，商品名称，类别，适用症状，适用类型保存到csv文件
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import codecs


url = "https://mall.jd.com/index-1000015441.html?cu=true&utm_source=baidu-search&utm_medium=cpc&utm_campaign=t_262767352_baidusearch&utm_term=113098950926_0_f4806f9c0e2e48bab760aa196dddf56c"
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 60)
browser.get(url)
browser.maximize_window()
btns = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="Map_m"]/area'))
)
d_url = []
results = ""
for i in btns:
    d_url.append(i.get_attribute("href"))
for i in d_url:
    browser.get(i)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500);')
    total = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b"))
    )
    total = int(total[0].text)
    print("页数：", total)
    s_urls = []
    for z in range(total - 1):
        shops = wait.until(#找到所有商品的a标签
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.gl-item>div>div.p-img>a"))
        )
        for j in shops:
            s_urls.append(j.get_attribute("href"))#找到所有商品的url
        next_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.pn-next"))
        )

        action = ActionChains(browser)
        action.move_to_element(next_btn).click().perform()
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500);')
        time.sleep(1)
    shops = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.gl-item>div>div.p-img>a"))
    )
    for j in shops:
        s_urls.append(j.get_attribute("href"))
    print("该分类商品数", len(s_urls))
    for j in s_urls:
        browser.get(j)
        browser.execute_script('window.scrollTo(0,1000);')
        title = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sku-name"))
        )
        title = title[0].text.strip()
        price = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.p-price>span"))
        )
        price = price[0].text + price[1].text
        pp = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul#parameter-brand>li>a"))
        )
        pp = pp[0].text.strip()
        res = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.parameter2.p-parameter-list>li"))
        )
        name = ''
        type = ''
        zz = ''
        s_type = ''
        for a in res:
            a0 = a.text.split("：")
            a1 = a0[0]
            a2 = a0[1]
            if a1 == "商品名称":
                name = a2
            elif a1 == "类别":
                type = a2
            elif a1 == "适用症状":
                zz = a2
            elif a1 == "适用类型":
                s_type = a2
        result = f"标题:{title}，价格:{price}，品牌:{pp}，商品名称:{name}，类别:{type}，适用症状:{zz}，适用类型:{s_type}"
        print(result)
        print("*" * 170)
        results += result + '\n'
        time.sleep(1)
    time.sleep(2)
with codecs.open('dyf.csv', 'a', encoding='utf-8') as file:
    wr = csv.writer(file)
    wr.writerow([results])
