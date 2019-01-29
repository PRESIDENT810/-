from selenium import webdriver
import time

"""
url: the douban page we will get html from
loadmore: whether or not click load more on the bottom 
waittime: seconds the broswer will wait after intial load and 
"""
def getHtml(url, loadmore = True, waittime = 2):
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    if loadmore:
        while True:
            try:
                next_button = browser.find_element_by_class_name("more")
                next_button.click()
                time.sleep(waittime)
            except:
                break
    html = browser.page_source
    browser.quit()
    return html