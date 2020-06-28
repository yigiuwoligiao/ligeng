from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import random


def main():
    browser = webdriver.Chrome()
    browser.maximize_window()
    opt = webdriver.ChromeOptions()
    actions = ActionChains(browser)

    wait = WebDriverWait(browser, 10)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    url = 'https://fresh.jd.com/'
    browser.get(url)

    more = browser.find_element_by_xpath('//dd[contains(@class,"cate_con")]//a[text()="更多"]')

    browser.execute_script("arguments[0].style.display = 'none'; return arguments[0];", more)

    # 获取首页分类栏全部品种的url
    shop_list_url = []
    shop_list = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//dd[contains(@class,"cate_con")]//a'))
    )
    # for i in shop_list:
    #     shop_list_url.append(i.get_attribute('href'))
    for i in shop_list:
        i=i.get_attribute('href')
        if len(i)>70:
            shop_list_url.append(i)


    # 根据首页分类url,进一步解析
    for j in shop_list_url:
        browser.get(j)
        # 向下滚动到底部
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500)')
        # 在下一页按钮旁边获取总页数
        # next_btn=wait.until(
        #     EC.presence_of_all_elements_located((By.XPATH,'//span[@class="p-skip"]/em/b'))
        # )
        # next_btn=int(next_btn[0].text())
        # print(next_btn)
        fenlei = browser.find_elements_by_class_name('search-key')[0]
        fenlei=fenlei.text.strip()
        print('当前品种-------', fenlei)
        ls = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="J_goodsList"]/ul/li[@class="gl-item"]'))
        )

        time.sleep(1)
        for item in ls:
            title = item.find_elements_by_xpath('.//div[@class="p-name p-name-type-2"]/a/em')[0]
            title = title.text.strip()
            print('标题:', title)
            price = item.find_elements_by_xpath('.//div[@class="p-price"]/strong/i')[0]
            price = ''.join(price.text).strip()
            print('价格:', price)
            # 取得是评价数,趋于真实销量
            xiaoliang = item.find_elements_by_xpath('.//div[@class="p-commit"]/strong/a')[0]
            xiaoliang = xiaoliang.text.strip()
            print('销量:', xiaoliang)
            store = item.find_elements_by_xpath('.//div[@class="p-shop"]/span/a')
            if len(store) >0:
                print('店铺:', store[0].text.strip())
            else:
                store='空'
                print('店铺:', store)
            img = item.find_elements_by_xpath('.//div[@class="p-img"]/a/img')[0]
            img = img.get_attribute('src')
            print('图片链接:', img)
            print('=' * 200)
            # 翻页处理
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500);')
            next_page_btn = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pn-next'))
            )
            print('next page...')
            action = ActionChains(browser)
            action.move_to_element(next_page_btn).click().perform()
            time.sleep(random.random() * 2)


if __name__ == '__main__':
    main()
