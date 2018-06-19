
import json

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

results = []


def parse(response):
    for comment in response.css('div.comment-list-item'):

        result={}

        print(comment)
        username=comment.xpath('.//a[@class="username"]/text()').extract_first().strip()
        result['username']=username
        contents = comment.xpath('.//div[@class="comment-item-content markdown-box"]/p/text()').extract()
        content_str=''
        for content in contents:
            content_str+=content.strip()


        result['content']=content_str

        results.append(result)


def has_next_page(response):

    print(response)
    comment_box=response.xpath('//div[@class="comment-box"]')
    item=comment_box.xpath('.//ul[@class="pagination"]').extract()

    if "disabled next-page" in item[0]:
        print('*'*10,'disabled next-page')
        return False
    else:
        return True


def goto_next_page(driver):

    element = driver.find_element_by_xpath("//li[@class='next-page']")
    element.click()
    print('*'*10,'next page')



def wait_page_return(driver, page):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )


def spider():

    driver = webdriver.PhantomJS()

    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:

        wait_page_return(driver, page)

        html = driver.page_source

        response = HtmlResponse(url=url, body=html.encode('utf8'))

        parse(response)

        if not has_next_page(response):
            break

        page += 1
        goto_next_page(driver)

    with open('/home/shiyanlou/comments.json', 'w') as f:
    # with open('comments.json', 'w') as f:
        f.write(json.dumps(results))


if __name__ == '__main__':
    spider()