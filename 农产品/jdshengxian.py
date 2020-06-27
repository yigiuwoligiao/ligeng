from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

def main():
    browser=webdriver.Chrome()
    action=webdriver.ChromeOptions()
    url='https://fresh.jd.com/'
    browser.get(url)
    print()


if __name__ == '__main__':
    main()







