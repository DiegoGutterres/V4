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
document = pd.read_excel('info.xlsx')
print(document.head)

#driver
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)
driver = webdriver.Chrome(options=options)
driver.get("https://app.contaazul.com/#/financeiro/contas-a-receber?view=revenue&amp;source=Financeiro%20%3E%20Contas%20a%20Receber&source=Menu%20Principal")

<<<<<<< HEAD
#inicio da automação
# driver.maximize_window()
# driver.execute_script("document.body.style.zoom='80%'")

while True:
    try:
        control = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody')
        if (control):
            break
    except:
        time.sleep(5)

#exibir
exibir = driver.find_element(By.XPATH, '//*[@id="type-filter-controller"]/span')
exibir.click()
time.sleep(2)

#recebido
recebido = driver.find_element(By.XPATH, '//*[@id="typeFilterContainer"]/li[4]/a/span[1]')
recebido.click()
time.sleep(1)

#aplicar
aplicar = driver.find_element(By.XPATH, '//*[@id="type-filter"]/ul/li[2]/div/button')
aplicar.click()
time.sleep(10)

#filtrar contas
contas = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/button')
contas.click()

all = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/li[1]/a/span[1]')
all.click()
time.sleep(1)

bradesco = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[2]/a/span')
bradesco.click()

itau = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[3]/a/span')
itau.click()

sap = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[4]/a/span')
sap.click() 

sicredi = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[5]/a/span')
sicredi.click()

inadimplente = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[10]/a/span')
inadimplente.click()

nova_data = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[16]/a/span')
nova_data.click()

renovacao = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[42]/a/span')
renovacao.click()

aplicar_contas = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/li[3]/div/button')
aplicar_contas.click()
time.sleep(10)
 
#filtrar data
data = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/button/span')
data.click()

todos = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/ul/li[5]/a')
todos.click()
time.sleep(10)

# --------- #

def func(i):
    pesquisar = driver.find_element(By.XPATH, '//*[@id="textSearch"]')
    pesquisar.send_keys(document['nome'][i])
    time.sleep(4)

for i in document['nome']:
    func(i)
=======
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
>>>>>>> dbc3f0ca65ee34dee624ca016ecd15bafb08ff4c

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
	

    
    
    
