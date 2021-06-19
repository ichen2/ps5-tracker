from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        
import time
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(executable_path='./chromedriver')#, options=options)
driver.implicitly_wait(5)

TARGET_URL = "https://www.target.com/p/playstation-5-console/-/A-81114595"
BEST_BUY_URL = "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"

found_at_target = False
found_at_best_buy = False

def isFound():
    global found_at_best_buy
    global found_at_target
    return found_at_target or found_at_best_buy

def checkTarget():
    global found_at_target
    print("Checking Target...")
    driver.get(TARGET_URL)
    found_at_target = "Sold out" not in driver.page_source
    print("Found at Target!" if found_at_target else "Not Found")

def checkBestBuy():
    global found_at_best_buy
    print("Checking Best Buy...")
    driver.get(BEST_BUY_URL)
    try:
        driver.find_element_by_xpath('//button[contains(text(), "Sold Out")]')
        print("Not Found")
    except NoSuchElementException:
        print("Found at BestBuy!")

while not isFound():
    checkTarget()
    checkBestBuy()
    time.sleep(2)


message = client.messages \
                .create(
                     body="PS5 Found!! " + TARGET_URL if found_at_target else BEST_BUY_URL,
                     from_=os.environ['TWILIO_PHONE_NUMBER'],
                     to=os.environ['MY_PHONE_NUMBER']
                 )