from selenium import webdriver
from selenium.webdriver.chrome.service import Service

path = 'C:/Users/brand/Downloads/chromedriver/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=path)

def get_brandywine_menu():
    brandywine = "https://uci.campusdish.com/en/locationsandmenus/brandywine/"
    driver = webdriver.Chrome(service=service)
    driver.get(brandywine)
    item_xpath = '//h3[contains(@class, "HeaderItemName")]'

    file = _create_file("BrandywineMenu.txt", "Brandywine's Food Options!")

    items = driver.find_elements(by='xpath', value = item_xpath)
    _fill_out_menu(items, file)
    file.close()
    driver.close()
    return file

def get_anteatery_menu():
    anteatery = "https://uci.campusdish.com/en/locationsandmenus/theanteatery/"
    driver = webdriver.Chrome(service=service)
    driver.get(anteatery)
    item_xpath = '//span[contains(@class, "HeaderItemNameLink")]'

    file = _create_file("AnteateryMenu.txt", "Anteatery's Food Options!")
    items = driver.find_elements(by='xpath', value = item_xpath)
    _fill_out_menu(items, file)
    file.close()
    driver.close()
    return file


def _create_file(name: str, title: str):
    file = open(name, "w")
    file.write(f"{title}\n")
    file.write("-----------------------------\n")
    return file

def _fill_out_menu(info: list[str], f: str):
    for item in info:
        f.write(f"{item.text}\n")
    
    f.write("-----------------------------\n")

def main():
    get_anteatery_menu()
    get_brandywine_menu()