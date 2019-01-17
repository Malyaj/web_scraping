SSO = "503048674"
key = "ssap@7878ge"

import os
from selenium import webdriver


chromedriver_path = r"D:\Users\703143501\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"
# https://sites.google.com/a/chromium.org/chromedriver/
# keep chromedriver.exe in PATH
# "D:\Users\703143501\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"

wf = 170164299
url = f"http://supportcentral.ge.com/caseforms/sup_myforms.asp?form_doc_id={wf}"

download_path = r"D:\Users\703143501\Downloads"
options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory={d}".format(d=download_path))

# initializing the driver
driver = webdriver.Chrome(options=options)


driver.get(url)
username_field = driver.find_element_by_name("username")
password_field = driver.find_element_by_name("password")
username_field.send_keys(SSO)
password_field.send_keys(key)
submit_field = driver.find_element_by_name("submitFrm")
submit_field.click()

xpath = """//*[@id="divCond_13756759"]/td[2]/a"""

elem = driver.find_element_by_xpath(xpath)

print(elem.text)

# closing the browser
driver.close()



