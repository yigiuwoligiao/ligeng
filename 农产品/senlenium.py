from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import csv
import codecs
import re



def main():
    # option = ChromeOptions()
    # option.add_argument('--headless')
    # browser = webdriver.Chrome(options=option)

    browser = webdriver.Chrome()
    browser.maximize_window()

    actions = ActionChains(browser)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    browser.get(
        'https://s.taobao.com/search?q=贝类&loc=杭州')

    name = browser.find_element_by_id('fm-login-id')
    passw = browser.find_element_by_id('fm-login-password')

    name.send_keys('路路的husband')
    time.sleep(1)
    passw.send_keys('LLL.4251020')
    wait=WebDriverWait(browser, 10)

    btn =wait.until(
        EC.visibility_of_element_located((By.ID, 'nc_1_n1z'))
    )

    actions.drag_and_drop_by_offset(btn, 260, 5).perform()
    time.sleep(1)

    # 两种写法选其一
    submit_btn = browser.find_element_by_class_name('fm-btn')
    submit_btn.click()
    # js2 = "var q=document.getElementByClass('fm-btn').click()"
    # browser.execute_script(js2)

    time.sleep(5)
    ls = wait.until(
        EC.visibility_of_element_located((By.ID, "mainsrp-itemlist"))
    )
    time.sleep(0.5)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight-500)")

    page_num = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "total"))
    )

    page_num = page_num[0].text.split(' ')
    page_num = int(page_num[1])
    print('列表总页数', page_num)

    s_urls = []#商品的具体url
    for i in range(page_num - 1):
        shops = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="item J_MouserOnverReq  "]/div[1]/div/div[1]/a'))
        )
        for j in shops:#所有商品
            s_urls.append(j.get_attribute("href"))
        next_btn=wait.until(#下一页按钮
            EC.presence_of_element_located((By.XPATH,'//li[@class="item next"]'))
        )
        next_btn.click()#翻页操作
        time.sleep(1)
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500);')
        time.sleep(1)
    shops = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="item J_MouserOnverReq  "]/div[1]/div/div[1]/a'))
    )
    for j in shops:
        s_urls.append(j.get_attribute("href"))
    print('该分类商品数量',len(s_urls))

if __name__ == '__main__':
    main()







