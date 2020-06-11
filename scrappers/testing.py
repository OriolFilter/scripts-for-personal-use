# https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python

from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("http://avi.im/stuff/js-or-no-js.html")
p_element = driver.find_element_by_id(id_='intro-text')
print(p_element.text)