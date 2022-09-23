import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from NotificationManager import NotificationManager as NM
load_dotenv()

scriptPath = os.path.dirname(__file__)

new_dict = {
    "date": {},
    "type": {}
}

try:
    df = pd.read_csv(f"{scriptPath}/schedule.csv")
    gameSchedule = df.to_dict()
except:
    gameSchedule = {
    "date": {},
    "type": {}
}

options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.reftown.com/games.asp?openonly=1")
driver.find_element(By.NAME, "Username").send_keys(os.getenv('EMAIL'))
driver.find_element(By.NAME, "Password").send_keys(os.getenv('PASSWORD'))
driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/form/p[5]/input").click()
WebDriverWait(driver, 30).until(EC.url_changes("https://www.reftown.com/login.asp"))
html = driver.page_source
MySoup = BeautifulSoup(html, "html.parser")
results = MySoup.find_all(name="tr", class_="game")
driver.close()

i = 0
for result in results:
    gameInfo = result.find_next("td").find_next("td").find_next("td").getText()
    if "12u" in gameInfo.lower() or "14u" in gameInfo.lower():
        date = result.find_next("td").find_next("td").getText()
        link = result.find_next("a")
        new_dict["date"][i] = date
        new_dict["type"][i] = gameInfo
        if date not in gameSchedule["date"].values():
            dateToSend = datetime.strptime(date, "%a%m/%d/%Y%I:%M %p")
            dateToSend = datetime.strftime(dateToSend, '%a %m/%d at %I:%M %p')
            NM.send_text(f"New game found for {dateToSend}. {gameInfo[3:]} register at https://www.reftown.com/{link['href']}")
        i += 1


df = pd.DataFrame(new_dict)
df.to_csv(f"{scriptPath}/schedule.csv", index=False)
