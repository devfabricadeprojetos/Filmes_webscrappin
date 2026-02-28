import requests
import pandas as pd
import time
import random
import sqlite3
from bs4 import Beautifulsoup
import datetime
from config import *

#pip install bs4 para instalar 

for pagina in range(1, paginalimite + 1):
    url = f"{base_url}?page={pagina}"

#https://www.adorocinema.com/filmes/numero-cinemas/?page=2

    print(f"Coletando dados da pagina {pagina} \n URL: {url}")
    resposta = requests.get(url,headers=headers)

    if resposta.status_code !=200:
        print(f'Erro ao carregar a pagina {pagina}.Codigodo erro é: {resposta.status_code}')

    soup = Beautifulsoup(resposta.text, 'html.parser')
    cards = soup.find_all("div", class_="card entity-card entity-card-list cf")

    for card in card:
        try:
            # tenta capturar o titulo do filme e o hiperlink da pagina do filme 
            titulo_tag = card.find('a', class_="meta-title-link")
            titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
            link = "http:// www.adorocinema.com/filmes/" + titulo_tag['href'] if titulo_tag else None

            #captura a nota do filme 
            nota_tag = card.find("span", class_= "stareval-note")
            nota = nota_tag.text.strip().replace(',','.') if nota_tag else "N/A"

            if link:
                filme_resposta = requests.get(link, headers=headers)

                if resposta.status_code ==200:
                    filme_soup = Beautifulsoup(filme_resposta.text, "html.parser")
                    diretor_tag = filme_soup.find("div, class_=meta-body-item meta-body-direction meta-body-oneline")
                    if diretor_tag:
                        diretor = (
                            diretor_tag.text
                            .strip()
                            .replace('Direção','')
                            .replace(',','')
                            .replace('|','')
                            .replace('\n','')
                            .replace('\r','')
                            .strip()
                    )
                    genero_block = filme_soup.find('div', class_='meta-body-info')
            if genero_block:
                genero_link = genero_block.find_all('a')
                generos = [g.text.strip() for g in genero_link]
                categoria = ", ".joing(generos[:3] if generos else "N/A")
            else:
                categoria = "N/A" 

        except Exception as erro:
            print(f"Erro ao processar o filme {titulo}. Erro: {erro}")