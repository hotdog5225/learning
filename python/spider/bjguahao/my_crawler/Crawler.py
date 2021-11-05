from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidCookieDomainException


class ICrawler(object):
    def get_html(self, url):
        return ""


class BJGuaHaoCrawler(object):
    def get_html_homepage(self, url):
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

    def add_cookie_to_driver(self, driver, url, cookie_dict):
        try:
            # to avoid InvalidCookieDomainException: https://stackoverflow.com/questions/59877561/selenium-common-exceptions-invalidcookiedomainexception-message-invalid-cookie
            driver.get(url)

            # set cookie
            for key, value in cookie_dict.items():
                driver.add_cookie({
                    'name': key,
                    'value': value,
                    'domain': ".114yygh.com",
                    'path': '/',
                    'httpOnly': True,
                })
            return driver
        except Exception as e:
            print(e)
            exit()

    def get_html_dept_detail(self, url, week_desc, cookies_dict):
        # 动态网页抓取
        driver = wb.Chrome()
        driver = self.add_cookie_to_driver(driver, url, cookies_dict)
        driver.get(url)

        # 等待要抓取的元素
        driver.implicitly_wait(20)
        try:
            # 点击可挂号的日期
            date_tag = driver.find_element(By.XPATH, '//span[@class="week" and text()="{}"]'.format(week_desc))
            date_tag.click()
            # 点击可挂号的上下午
            available_button_tag_list = driver.find_elements(By.XPATH, "//div[contains(text(),'剩余')]")  # 可挂号的button
            for but_tag in available_button_tag_list:
                but_tag.click()
            driver.find_elements(By.XPATH, "//div[@class='el-scrollbar__view']/div[contains(@class, 'list-item')]")
        except Exception as e:
            print(e)
            exit()

        html = driver.page_source
        driver.quit()
        return html

    def appointment(self, headers, cookies):
        return
