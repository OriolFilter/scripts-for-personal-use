# from selenium import webdriver
from time import sleep
import pathlib
from selenium import webdriver

web = webdriver.Firefox(executable_path=(str(pathlib.Path(__file__).parent)+'/geckodriver'))
web.get('https://ouo.press/jt16Yo')
sleep(3)
web.execute_script("document.forms[0].submit()")
sleep(10)
web.execute_script("document.forms[0].submit()")
sleep(5)
print(web.current_url)
web.close()
# browser = webdriver.Firefox()
# browser.get('http://seleniumhq.org/')

#https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path