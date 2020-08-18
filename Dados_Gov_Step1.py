# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 02:53:04 2020

@author: vroque
"""

import requests
from bs4 import BeautifulSoup
from aux_functions import get_page_number
import pandas as pd
import re

"""<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
' Mapeando as organizações: navegando pela página onde estão disponíveis as informações
' das instituições que divulgam seus dados na plataforma de dados abertos. 
O objetivo é identificar todas a organizações listadas no site dados.gov.br
"""

main_site = 'http://www.dados.gov.br/organization'

nPg = get_page_number(main_site)
print(nPg)


# A estrutura das páginas onde estão o conjunto das instituições é 
#representado pela variavel radical

radical = 'http://www.dados.gov.br/organization?q=&sort=&page='

pages = [] # lista de páginas onde são organizadas as informações das instituições
setlis = [] # conjunto de 'li', tag do html onde estão as informações 
orgs = [] # root data das organizações
nPg = nPg + 1 # soma 1 por conta da função range


# Loop pra gerar os links das páginas exemplo:
# http://www.dados.gov.br/organization?q=&sort=&page=2
for p in range(1,nPg):
    site = radical + str(p)
    pages.append(site)


# Capturando o root data das páginas armazenadas em 'pages', lista gerada no loop anterior
for site in pages:
    r = requests.get(site)
    
    page_source = r.text
    
    soup = BeautifulSoup(page_source, 'html.parser')
    
 
    li = soup.find_all("li")
    
    for x in li:
        setlis.append(str(x))
        
        
        
# Captura tag com a class especifica que armazena as informações relevantes
for div in setlis: 
    if 'media-item' in div: orgs.append(div)
    
    
# Capturando as informações específicas
page_info = []
for org in orgs:
          # Definindo Nome da instituição
    headlist = []
    sthead = org.find('heading">')+ 9
    endhead =  sthead + 120
    head = org[sthead:endhead]
    head = head[0:head.find('</h3>')]
           
            # Definindo Link
    linklist = []
    stlink = org.find('href="')+ 6
    endlink =  stlink + 150 #inst.find('</')
    link = org[stlink:endlink]
    link = link[0:link.find('"')]
          
          
            # Definindo o conjunto de informaçoes - número
            
    stnumInfo = org.find('class="count">')+14
    ennumInfo =  stnumInfo + 24
    numInfo = org[stnumInfo:ennumInfo]
    numInfo = numInfo[0:numInfo.find('</')]
    infos = [head, link, numInfo]
#page_info é o resultado, sendo uma lista de informações, o nome da organização, 
#o link e o número de informações disponíveis
    page_info.append(infos)
    


# Gerando o dataframe para exportar para um arquivo em formato ".xlsx"
df = pd.DataFrame(page_info)


df.columns = ['Instituição','Link','Num_dados']

df['Num_dados_int'] = df['Num_dados'].apply(lambda dados: re.sub("\D","",dados))

df['Link'] = df['Link'].apply(lambda link: 'http://www.dados.gov.br' + link)

df.to_excel('Relação de Instituições - Dados.gov.xlsx')

