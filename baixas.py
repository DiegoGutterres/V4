#server
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#login automatico
from config import CHROME_PROFILE_PATH

#excel
import pandas as pd

#driver
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)
driver = webdriver.Chrome(options=options)
driver.get("https://app.contaazul.com/#/financeiro/contas-a-receber?view=revenue&amp;source=Financeiro%20%3E%20Contas%20a%20Receber&source=Menu%20Principal")

time.sleep(5)
#inicio da automação
data = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/button')
data.click()

semana = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/ul/li[2]/a')
semana.click()



time.sleep(30)