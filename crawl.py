# pluralsight.py
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


d = dict()

d['Chuyen muc'] = [] #[x[0].text.split("\n")[0] for x in tds]
d['Nhu cau'] = [] #[x[1].text.split("\n")[0] for x in tds]
d['Tinh/Thanh pho'] = [] #[x[2].text.split("\n")[0] for x in tds]
d['Quan/huyen'] = [] #[x[3].text.split("\n")[0] for x in tds]
d['Xa/Phuong'] = [] #[x[4].text.split("\n")[0] for x in tds]
d['Duong/khu vuc'] = [] #[x[5].text.split("\n")[0] for x in tds]
d['Gia'] = [] #[x[6].text.split("\n")[0] for x in tds]
d['Ngay dang'] = [] #[x[7].text.split("\n")[0] for x in tds]
d['Dien tich'] = [] #[x[8].text.split("\n")[0] for x in tds]
d['Huong'] = [] #[x[9].text.split("\n")[0] for x in tds]
d['So Tang'] = [] #[x[10].text.split("\n")[0] for x in tds]
d['So phong'] = [] #[x[11].text.split("\n")[0] for x in tds]
d['Nha ve sinh'] = [] #[x[12].text.split("\n")[0] for x in tds]
d['Giay to phap'] = [] #[x[13].text.split("\n")[0] for x in tds]
d['Dien thoai'] = [] #[x[14].text.split("\n")[0] for x in tds]
d['Mo ta'] = [] #[x[15].text.split("\n")[0] for x in tds]
def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    # driver = webdriver.Chrome(options = chrome_options)
    # For windows
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options = chrome_options)
    return driver


def crawl(driver, page):
    # Step 1: Go to pluralsight.com, category section with selected search keyword
    if page == 0:
        url = 'http://www.laydulieu.com/nha-dat/'
    else :
        url = 'http://www.laydulieu.com/nha-dat/?page=' + str(page)
    #driver.get(f"https://www.pluralsight.com/search?q={search_keyword}&categories=course")
    driver.get(url)
    # wait for the element to load
    try:
        WebDriverWait(driver, 15).until(lambda s: s.find_element_by_id("_list_data").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None
    print("some data :D at page : ", page+1)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate over the search result and fetch the course
    section = soup.find_all("section")[0]#.select("div.row")[2]
    row = section.select("div.row")[2]
    data = row.select("div.col-md-24")[0]
    tb_data = data.select("div.tb-data")[0]
    tb_head = data.select("div.tb-head")[0]
    rows_data = tb_data.find_all(lambda tag: tag.name == 'tr')
    rows_head = tb_head.find_all(lambda tag: tag.name == 'tr')

    tds = [x.find_all(lambda tag: tag.name == 'td') for x in rows_data] 
    # heads = rows_head[0].find_all(lambda tag: tag.name == 'td')

    d['Chuyen muc'] = d['Chuyen muc'] + [x[0].text.split("\n")[0] for x in tds]
    d['Nhu cau'] = d['Nhu cau'] + [x[1].text.split("\n")[0] for x in tds]
    d['Tinh/Thanh pho'] = d['Tinh/Thanh pho'] + [x[2].text.split("\n")[0] for x in tds]
    d['Quan/huyen'] = d['Quan/huyen'] + [x[3].text.split("\n")[0] for x in tds]
    d['Xa/Phuong'] = d['Xa/Phuong'] + [x[4].text.split("\n")[0] for x in tds]
    d['Duong/khu vuc'] = d['Duong/khu vuc'] + [x[5].text.split("\n")[0] for x in tds]
    d['Gia'] = d['Gia'] + [x[6].text.split("\n")[0] for x in tds]
    d['Ngay dang'] = d['Ngay dang'] + [x[7].text.split("\n")[0] for x in tds]
    d['Dien tich'] = d['Dien tich'] + [x[8].text.split("\n")[0] for x in tds]
    d['Huong'] = d['Huong'] + [x[9].text.split("\n")[0] for x in tds]
    d['So Tang'] = d['So Tang'] + [x[10].text.split("\n")[0] for x in tds]
    d['So phong'] = d['So phong'] + [x[11].text.split("\n")[0] for x in tds]
    d['Nha ve sinh'] = d['Nha ve sinh'] + [x[12].text.split("\n")[0] for x in tds]
    d['Giay to phap'] = d['Giay to phap'] + [x[13].text.split("\n")[0] for x in tds]
    d['Dien thoai'] = d['Dien thoai'] + [x[14].text.split("\n")[0] for x in tds]
    d['Mo ta'] = d['Mo ta'] + [x[15].text.split("\n")[0] for x in tds]
    
# create the driver object.
driver = configure_driver()
for page in range(9000):
    crawl(driver, page)
# close the driver.
driver.close()

df = pd.DataFrame(d)
df.to_csv("9000_pages.csv",encoding='utf-8-sig')
