#server
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date 
from api.api import main

valores, sheet = main()


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
options.add_experimental_option(
    'prefs', {
        "profile.managed_default_content_settings.images": 2,
    }
)
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
driver.find_element(By.XPATH, '//*[@id="type-filter-controller"]/span').click()
time.sleep(0.5)

#recebido
driver.find_element(By.XPATH, '//*[@id="typeFilterContainer"]/li[4]/a/span[1]').click()

#aplicar
driver.find_element(By.XPATH, '//*[@id="type-filter"]/ul/li[2]/div/button').click()
time.sleep(5)

#filtrar contas
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/button').click()

#all
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/li[1]/a/span[1]').click()
time.sleep(0.3)

#bradesco
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[2]/a/span').click()

#itau
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[3]/a/span').click()

#sap
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[4]/a/span').click()

#sicredi
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[5]/a/span').click()

#churn provavel
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[9]/a/span').click()

#inad
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[10]/a/span').click()

#franq inad
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[11]/a/span').click()

#nova data
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[16]/a/span').click()

#renovaçao
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[42]/a/span').click()

#aplicar
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/li[3]/div/button').click()
time.sleep(5)
 
#ir para cima
driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL, Keys.HOME)
time.sleep(.5)

#filtrar data
driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/button/span').click()

#mostrar todos
driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/ul/li[5]/a').click()
time.sleep(6)

# --------- #

def carregando():
    while True:
        loading = driver.find_element(By.XPATH, '//*[@id="loading"]').get_attribute('style')
        if loading == 'display: block;':         
            print('sleeping')
            time.sleep(5)
        else:
            break

def func(cliente):
    pesquisar = driver.find_element(By.XPATH, '//*[@id="textSearch"]')
    pesquisar.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
    pesquisar.send_keys(document['CLIENTE'][cliente])
    pesquisar.send_keys(Keys.ENTER)

    carregando()

    #checar se tem que dar enter dnv
    if driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/div/div[1]/b[2]/b').text not in driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[4]/div[1]/span[1]').text:
        pesquisar.send_keys(Keys.ENTER)
        carregando()

    #ver se existe um lançamento
    exist = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[4]/div[1]').is_displayed()
    if exist == False:
        return
    print(document['CLIENTE'][cliente])

 
    #se o valor for mt diferente ele vai só pular pro proximo
    valor = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[5]/div[2]')
    
    # -- tem que transformar em float para conseguir comparar --
    valor_f = valor.text
    valor_formatado = valor_f.replace('.', '').replace(',','.')
    valor_p = document['VALOR'][cliente].replace('.', '').replace(',','.')
    
    sobra = float(valor_p) - float(valor_formatado)
    if (sobra < 0.0 or sobra > 30.0):
        return
    
    #abrir
    try: 
        driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[4]/div[1]/span[1]').click()
        time.sleep(3)
    except:
        return        


    #conta azul funciona por id de conta, não pelo nome! (conta itau: 29329659)
    conta = driver.find_element(By.XPATH, '//*[@id="newIdConta"]')
    banco = driver.find_element(By.XPATH, '//*[@id="idBanco"]').get_attribute('value')
    if banco != '29329659': #teste com a conta do bradesco
        conta.click()
        conta.send_keys(Keys.CONTROL, 'A', Keys.DELETE)
        conta.send_keys('01.0 [Espelho Itaú] Receitas/Despesas FLUXO')
        # conta.send_keys(Keys.ENTER)
        
        time.sleep(2)    

    #data
    today = date.today()
    data_formatada = today.strftime("%d%m%Y")
    data_atual = driver.find_element(By.XPATH, '//*[@id="dtVencimento"]')
    data_atual.click()
    data_atual.send_keys(data_formatada)

    #recebido
    driver.find_element(By.XPATH, '//*[@id="formStatement"]/div[2]/div[2]/div[2]/label[4]/div/span[1]').click()
    time.sleep(2)
    
    #multa
    if sobra == 0.0:
        None
    elif sobra < 1:
        sobra_decimal = '{:.2f}'.format(sobra).lstrip('0')
        driver.find_element(By.XPATH, '//*[@id="interest"]').send_keys(',' + sobra_decimal)
    else:
        driver.find_element(By.XPATH, '//*[@id="interest"]').send_keys('{:.2f}'.format(sobra).replace('.', ','))
    time.sleep(3)

    #salvar
    driver.find_element(By.XPATH, '//*[@id="finance-save-options"]/div[1]/button[2]').click()
    time.sleep(1)
    
    try:
        #popup dps de clicar pra salvar
        driver.find_element(By.XPATH, '//*[@id="newPopupManagerReplacement"]/div[3]/a[1]').click()
        time.sleep(5)
    except:
        None
        
    time.sleep(5)
    print(f'{document["CLIENTE"][cliente]}')
    
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
        else: 
            cliente = 0
    break

for l in range(len(document['CLIENTE'])):
    func(cliente)
    cliente += 1

driver.quit()