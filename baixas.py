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
            time.sleep(1)
            break
    except:
        time.sleep(2)

#exibir
driver.find_element(By.XPATH, '//*[@id="type-filter-controller"]/span').click()
time.sleep(.5)

#recebido
driver.find_element(By.XPATH, '//*[@id="typeFilterContainer"]/li[4]/a/span[1]').click()

#aplicar
driver.find_element(By.XPATH, '//*[@id="type-filter"]/ul/li[2]/div/button').click()
time.sleep(3)

#filtrar contas
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/button').click()

#all
#listar a ordem e largar num loop
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

#cartao iugu
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[35]/a/span').click()

#renovaçao
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/div/li[42]/a/span').click()

#aplicar
driver.find_element(By.XPATH, '//*[@id="bank-filter"]/ul/li[3]/div/button').click()
time.sleep(3)

#ir para cima
driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL, Keys.HOME)
time.sleep(1)

#filtrar data
driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/button/span').click()

#mostrar todos
driver.find_element(By.XPATH, '//*[@id="financeTopFilters"]/div[2]/ul/li[5]/a').click()
time.sleep(3)

# --------- #
finished = 0

def carregando():
    while True:
        loading = driver.find_element(By.XPATH, '//*[@id="loading"]').get_attribute('style')
        if loading == 'display: block;':
            #print('sleeping')
            time.sleep(3)
        else:
            break

def func(cliente):
    pesquisar = driver.find_element(By.XPATH, '//*[@id="textSearch"]')
    pesquisar.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
    try:
        pesquisar.send_keys(document['CLIENTE'][cliente])
        pesquisar.send_keys(Keys.ENTER)
        carregando()
    except:
        finished += 1
        return

    #ver se existe um lançamento
    exist = driver.find_element(By.XPATH, '//*[@id="conteudo"]/div/div[2]/div[2]/div/div[6]').get_attribute("style")
    if exist == "display: none;":
        print('none')
        return

    #checar se tem que dar enter dnv
    try:

        if driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/div/div[1]/b[2]/b').text not in driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[4]/div[1]/span[1]').text:
            pesquisar.send_keys(Keys.ENTER)
            carregando()
    except:
            pesquisar.send_keys(Keys.ENTER)
            carregando()
    #se o valor for mt diferente ele vai só pular pro proximo
    valor = driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[5]/div[2]')

    # -- tem que transformar em float para conseguir comparar --
    valor_f = valor.text
    if '.' in valor_f:
        valor_formatado = valor_f.replace('.', '').replace(',','.')
    else:
        valor_formatado = valor_f.replace(',','.')

    valor_p = document['VALOR'][cliente].replace('.', '').replace(',','.')
    try:
        sobra = float(valor_p) - float(valor_formatado)
        if (sobra <= -5 or round(sobra) > float(valor_formatado) * 0.04 ):
            print('none')
            return
    except ValueError:
        print('none')
        return
    
    time.sleep(2)
    #abrir
    try:
        driver.find_element(By.XPATH, '//*[@id="statement-list-container"]/table[1]/tbody/tr[1]/td[4]/div[1]/span[1]').click()
        time.sleep(3)
    except KeyError:
        print('none')
        return

    #conta azul funciona por id de conta, não pelo nome! (conta itau: 29329659)
    conta = driver.find_element(By.XPATH, '//*[@id="newIdConta"]')
    banco = driver.find_element(By.XPATH, '//*[@id="idBanco"]').get_attribute('value')
    if banco != '29329659': #teste com a conta do bradesco
         conta.click()
         conta.send_keys(Keys.CONTROL, 'A', Keys.DELETE)
         conta.send_keys('01.0 [Espelho Itaú] Receitas/Despesas FLUXO')
         #conta.send_keys(Keys.ENTER)
    time.sleep(3)

    #data
    today = date.today()
    data_formatada = today.strftime("%d%m%Y")
    data_atual = driver.find_element(By.XPATH, '//*[@id="dtVencimento"]')
    data_atual.click()
    data_atual.send_keys(data_formatada)

    #recebido
    driver.find_element(By.XPATH, '//*[@id="formStatement"]/div[2]/div[2]/div[2]/label[4]/div/span[1]').click()
    time.sleep(.4)

    #multa
    if sobra == 0:
        None

    elif sobra < 1 and sobra >= 0.01:
        sobra_decimal = '{:.2f}'.format(sobra).lstrip('0')
        driver.find_element(By.XPATH, '//*[@id="interest"]').send_keys(',' + sobra_decimal)

    elif sobra < 0:
        sobra_desconto = '{:.2f}'.format(sobra).replace('.', ',')
        print(sobra_desconto)
        driver.find_element(By.XPATH, '//*[@id="discount"]').send_keys(sobra_desconto)

    elif sobra <= 5 and sobra >= -5:
        driver.find_element(By.XPATH, '//*[@id="valor"]').click
        for o in range(0,10): driver.find_element(By.XPATH, '//*[@id="valor"]').send_keys(Keys.BACKSPACE)
        valor_p_formatado = '{}'.format(valor_p).replace('.',',')
        driver.find_element(By.XPATH, '//*[@id="valor"]').send_keys(valor_p_formatado)

    else:
        driver.find_element(By.XPATH, '//*[@id="interest"]').send_keys('{:.2f}'.format(sobra).replace('.', ','))
    time.sleep(1.2)

    #salvar
    driver.find_element(By.XPATH, '//*[@id="finance-save-options"]/div[1]/button[2]').click()
    time.sleep(1)

    try:
        #popup dps de clicar pra salvar
        driver.find_element(By.XPATH, '//*[@id="newPopupManagerReplacement"]/div[3]/a[1]').click()
        time.sleep(3)
    except:
        None

    time.sleep(3)
    print(f'{document["CLIENTE"][cliente]}')

# --------- #

while True:
    transferencia = document['VALOR'].str.replace('.', '').str.replace(',','.')
    for i in range(len(transferencia)):
        valor_float = float(transferencia[i])
        print(float(transferencia[i]))

        if valor_float < -1000.00:
            print(f'transferencia de R${transferencia[i]}')
            cliente = i + 1
            break
        else:
            cliente = 0
    break

for l in range(len(document['CLIENTE'])):
    if finished == 3:
        driver.quit()
    func(cliente)
    cliente += 1

