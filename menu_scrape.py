from selenium import webdriver
from selenium.webdriver.chrome.service import Service

brandywine = "https://uci.campusdish.com/en/locationsandmenus/brandywine/"
path = 'C:/Users/brand/Downloads/chromedriver/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get(brandywine)

#station_xpath = '//h2[contains(@class, "StationHeaderTitle")]'
#category_xpath = '//h2[contains(@class, "CategoryName")]'
item_xpath = '//h3[contains(@class, "HeaderItemName")]'
#calorie_xpath = '//span[contains(@class, "ItemCalories")]'


items = driver.find_elements(by='xpath', value = item_xpath)
#calories = driver.find_elements(by='xpath', value = calorie_xpath)

file = open("fooditems.txt", "w")

for item in items:
    file.write(f"{item.text}\n")

