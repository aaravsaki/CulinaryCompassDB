from selenium import webdriver
from selenium.webdriver.chrome.service import Service

brandywine = "https://uci.campusdish.com/en/locationsandmenus/brandywine/"
anteatery = "https://uci.campusdish.com/en/locationsandmenus/theanteatery/"
path = 'C:/Users/brand/Downloads/chromedriver/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

def get_brandywine_menu():
    driver.get(brandywine)
    item_xpath = '//h3[contains(@class, "HeaderItemName")]'

    file = create_file("BrandywineMenu.txt", "Brandywine's Food Options!")

    items = driver.find_elements(by='xpath', value = item_xpath)
    fill_out_menu(items, file)
    file.close()

def get_anteatery_menu():
    driver.get(anteatery)
    item_xpath = '//span[contains(@class, "HeaderItemNameLink")]'

    file = create_file("AnteateryMenu.txt", "Anteatery's Food Options!")
    items = driver.find_elements(by='xpath', value = item_xpath)
    fill_out_menu(items, file)
    file.close()


def create_file(name: str, title: str):
    file = open(name, "w")
    file.write(f"{title}\n")
    file.write("-----------------------------\n")
    return file

def fill_out_menu(info: list[str], f: str):
    for item in info:
        f.write(f"{item.text}\n")

def main():
    get_anteatery_menu()
    get_brandywine_menu()

