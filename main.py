import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf4gl0EViL1axY2tJfhqRXGFrW4k0l6ZwUqtEkWRUtrmSoqAA/viewform?usp=sf_link"

# ------------------------------------------- SCRAPE ADS ------------------------------------------- #
response = requests.get(URL)

website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

link_tags = soup.find_all('a', class_='StyledPropertyCardDataArea-anchor', attrs={'data-test': 'property-card-link'})
links = [tag.get('href') for tag in link_tags]

price_tags = soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')
prices = [re.sub(r'[+/mo]', '', tag.get_text(strip=True)).split(" ")[0] for tag in price_tags]

address_tags = soup.find_all('address', attrs={"data-test": "property-card-addr"})
address_texts = [re.sub(r'[|]', '', tag.get_text(strip=True)).split("\n")[0] for tag in address_tags]

addresses = []
for address in address_texts:
    if address.count(",") == 3:
        address = address.split(",", 1)[1]
    addresses.append(address)

# ------------------------------------------- ENTRY FORM ------------------------------------------- #
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("disable-notifications")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(FORM)

for rental in range(len(addresses)):
    time.sleep(10)

    address_form = driver.find_element(
        By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    address_form.send_keys(addresses[rental])

    price_form = driver.find_element(
        By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    price_form.send_keys(prices[rental])

    link_form = driver.find_element(
        By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    link_form.send_keys(links[rental])

    send_button = driver.find_element(
        By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span'
    )
    send_button.click()
    time.sleep(3)

    other_answer = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    other_answer.click()


driver.quit()
