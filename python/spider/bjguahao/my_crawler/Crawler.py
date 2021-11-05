from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class ICrawler(object):
    def get_html(self, url):
        return ""


class BJGuaHaoCrawler(object):
    def get_html(self, url):
        # 动态网页抓取
        driver = wb.Chrome()
        driver.get(url)
        # 初始有一个向导, 随便点击一个元素关掉
        driver.find_element(By.TAG_NAME, "body").click()
        # 滚动条拉到底部 js
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # 页面下拉, 模拟按键page-down: 触发js执行
        bodyTag = driver.find_element(By.TAG_NAME, 'body')
        bodyTag.click()
        bodyTag.send_keys(Keys.PAGE_DOWN)

        # 确保某个元素存在(等待ajax加载完成)
        # 隐式等待
        try:
            driver.implicitly_wait(10)
            hosp_item_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'hos-item')]")
        except NoSuchElementException as e:
            print(e)
            exit()
        # 显示等待,10找不到就报错
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'hos-item')]")))

        # use bs4 to parse html
        html = driver.page_source

        # 退出driver
        driver.quit()

        return html

    def appointment(self, headers, cookies):
        return
