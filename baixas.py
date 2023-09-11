#server
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#login automatico
from config import CHROME_PROFILE_PATH
control = 0

#excel
import pandas as pd

#driver
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)
driver = webdriver.Chrome(options=options)
driver.get("https://app.contaazul.com/#/financeiro/contas-a-receber?view=revenue&amp;source=Financeiro%20%3E%20Contas%20a%20Receber&source=Menu%20Principal")

#ler a planilha
document = pd.read_excel('info.xlsx')
del document['Saldo Final']
del document['Tipo do documento']
del document['Código']
del document['Referência']
del document['E-mail']
del document['Histórico']

#inicio da automação
time.sleep(30)
#clicar pra abrir o filtro
data = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]')
data.click()

time.sleep(3)
#filtrar por semana
semana = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/ul/li[2]/a')
semana.click()
time.sleep(10)

#tirar o filtro de recebido para diminuir o tanto de lançametos
exibir = driver.find_element(By.XPATH, '//*[@id="type-filter-controller"]')
exibir.click()
time.sleep(2)

recebido = driver.find_element(By.XPATH, '//*[@id="typeFilterContainer"]/li[4]/a/span[1]')
recebido.click()
time.sleep(2)

aplicar = driver.find_element(By.XPATH, '//*[@id="type-filter"]/ul/li[2]/div/button')
aplicar.click()
time.sleep(5)

#abrir todos lançamentos 
while True:
    try:
        button = driver.find_element(By.XPATH, '//*[@id="conteudo"]/div/div[2]/div[2]/div/div[3]/button')
        button.click()
        time.sleep(10)
    except:
        break

#pegar o nome dos clientes com base na planilha

for each_client in document['Nome Cliente']:
    # try:
        print(each_client)  
        
        cliente = driver.find_element(By.XPATH, f'//span[contains(text(), "{each_client}")]') 
        cliente.click()
        time.sleep(10)
    # except:
    #     continue
	

    
    
    
