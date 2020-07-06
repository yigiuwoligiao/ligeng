from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import random
import pymysql
from selenium.webdriver.chrome.options import Options


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
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

    for i in shop_list:
        i = i.get_attribute('href')
        if len(i) > 70:
            shop_list_url.append(i)
    test_ll = ()
    # 根据首页分类url,进一步解析
    for j in shop_list_url:
        if len(j) > 0:
            browser.get(j)
            # 向下滚动到底部
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500)')

            variety = browser.find_elements_by_class_name('search-key')[0]
            variety = str(variety.text.strip().split('"')[1])
            print('当前品种-------', variety)

            # ls = wait.until(
            #     EC.presence_of_all_elements_located((By.XPATH, '//div[@id="J_goodsList"]/ul/li[@class="gl-item"]'))
            # )
            ls=browser.find_elements_by_xpath('//div[@id="J_goodsList"]/ul/li[@class="gl-item"]')
            time.sleep(1)
            if len(ls)>0:
                for item in ls:
                    title = item.find_elements_by_xpath('.//div[@class="p-name p-name-type-2"]/a/em')[0]
                    title = str(title.text.strip())
                    print('标题:', title)
                    detail_url = item.find_elements_by_xpath('.//div[@class="p-name p-name-type-2"]/a')[0]
                    detail_url = detail_url.get_attribute('href')
                    print('商品链接:', detail_url)
                    price = item.find_elements_by_xpath('.//div[@class="p-price"]/strong/i')[0]
                    price = ''.join(price.text).strip()
                    print('价格:', price)
                    # 取得是评价数,趋于真实销量
                    xiaoliang = item.find_elements_by_xpath('.//div[@class="p-commit"]/strong/a')[0]
                    xiaoliang = xiaoliang.text.strip()
                    print('销量:', xiaoliang)
                    store = item.find_elements_by_xpath('.//div[@class="p-shop"]/span/a')
                    if len(store) > 0:
                        store = store[0].text.strip()
                        print('店铺:', store)
                    else:
                        store = '空'
                        print('店铺:', store)
                    img = item.find_elements_by_xpath('.//div[@class="p-img"]/a/img')[0]
                    img = img.get_attribute('src')
                    print('图片链接:', img)
                    print('=' * 200)
                    test_ll = (variety, title, detail_url, price, xiaoliang, store, img)
                    # test_ls.append(variety)
                    # test_ls.append(title)
                    # test_ls.append(detail_url)
                    # test_ls.append(price)
                    # test_ls.append(xiaoliang)
                    # test_ls.append(store)
                    # test_ls.append(img)
            else:
                pass
        else:
            pass
    return test_ll

    '''
    翻页有问题
    '''
    # 翻页处理
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight-500);')
    next_page_btn = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'pn-next'))
    )
    print('next page...')
    action = ActionChains(browser)
    action.move_to_element(next_page_btn).click().perform()
    time.sleep(random.random() * 2)
    page_now = browser.find_element_by_xpath('//span[@class="p-skip"]/input[1]').get_attribute('value')
    print('当前爬完了', page_now)


def write(test_ll):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, db='ligeng', user='root', password='123456',
                               charset='utf8')
        cursor = conn.cursor()
        sql = 'insert into jdshengxian(variety,title,detail_url,price,seles,store,img_url) values(%s,%s,%s,%s,%s,%s,%s)'
        args = (test_ll)
        cursor.execute(sql, args=args)
        conn.commit()
        print('数据库保存成功')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start=time.time()
    test_ls = main()
    write(test_ls)
    end=time.time()
    print('用时',end-start)