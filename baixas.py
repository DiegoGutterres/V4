#server
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
from api.api import valores

#login automatico
from config import CHROME_PROFILE_PATH
control = 0

#excel
import pandas as pd
document = pd.DataFrame(valores, columns=valores[0]).drop(0,axis=0).reset_index(drop=True)
print(document.head)
document.set_index('DATA')

#driver
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)
#options.add_argument('--headless') doideira
driver = webdriver.Chrome(options=options)
driver.get("https://app.contaazul.com/#/financeiro/contas-a-receber?view=revenue&amp;source=Financeiro%20%3E%20Contas%20a%20Receber&source=Menu%20Principal")

#inicio da automação
while True:
    try:
        control = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody')
        if (control):
            break
    except:
        time.sleep(5)

#exibir
time.sleep(2)
exibir = driver.find_element(By.XPATH, '//*[@id="type-filter-controller"]/span')
exibir.click()
time.sleep(2)

#recebido
recebido = driver.find_element(By.XPATH, '//*[@id="typeFilterContainer"]/li[4]/a/span[1]')
recebido.click()
time.sleep(1)

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

franq_inad = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[11]/a/span')
franq_inad.click()

nova_data = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[16]/a/span')
nova_data.click()

renovacao = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[42]/a/span')
renovacao.click() 

aplicar_contas = driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/li[3]/div/button')
aplicar_contas.click()
time.sleep(10)
 
#ir para cima
up = driver.find_element(By.CSS_SELECTOR, 'body')
up.send_keys(Keys.CONTROL, Keys.HOME)
time.sleep(2)

#filtrar data
data = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/button/span')
data.click()

todos = driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/ul/li[5]/a')
todos.click()
time.sleep(10)

# --------- #

def func(cliente):
    pesquisar = driver.find_element(By.XPATH, '//*[@id="textSearch"]')
    pesquisar.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
    pesquisar.send_keys(document['CLIENTE'][cliente])
    pesquisar.send_keys(Keys.ENTER)

    time.sleep(10)
    loading = driver.find_element(By.XPATH, '//*[@id="loadCenter"]').get_attribute('class')
    while loading == 'progress progress-striped active loadCenterMaior':
        print('sleeping')
        time.sleep(10)


    valor = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[5]/div[2]')
    if (valor.text != document['VALOR'][cliente]):
        return    

    abrir = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[4]/div[1]/span[1]')
    abrir.click()
    time.sleep(4)

    #conta azul funciona por id de conta, não pelo nome! (conta itau: 29329659)
    conta = driver.find_element(By.XPATH, '//*[@id="newIdConta"]')
    banco = driver.find_element(By.XPATH, '//*[@id="idBanco"]').get_attribute('value')
    if banco != '29329659':
        conta.click()
        conta.send_keys(Keys.CONTROL, 'A', Keys.DELETE)
        conta.send_keys('01.0 [Espelho Itaú] Receitas/Despesas FLUXO')
        conta.send_keys(Keys.ENTER)

    today = date.today()
    data_formatada = today.strftime("%d%m%Y")
    data_atual = driver.find_element(By.XPATH, '//*[@id="dtVencimento"]')
    data_atual.click()
    data_atual.send_keys(data_formatada)

    btn_recebido = driver.find_element(By.XPATH, '//*[@id="formStatement"]/div[2]/div[2]/div[2]/label[4]/div/span[1]')
    btn_recebido.click()
    time.sleep(1)

    final = driver.find_element(By.XPATH, '//*[@id="modal-footer-statement"]/div/button')
    final.click()
    time.sleep(5)

# --------- #

while True:
    transferencia = document['VALOR'].str.replace('.', '').str.replace(',','.')
    for i in range(len(transferencia)):
        valor_float = float(transferencia[i])
        print(float(transferencia[i]))

        if valor_float < -1000.00:
            print(f'transferencia de R${transferencia[i]}')
            cliente = i
            break
    break

for l in range(len(document['CLIENTE'])):
    cliente += 1
    func(cliente)




    
    
    
