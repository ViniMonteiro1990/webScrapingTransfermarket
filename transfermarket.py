import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

ListaJogadores = []
ListaIdade = []
ListaPosicao = []
ListaNacionalidade = []
ListaValor = []
for r in range(1, 11):
    pagina = f'https://www.transfermarkt.com.br/spieler-statistik/wertvollstespieler/marktwertetop/statistik?saison_id=alle&land_id=0&ausrichtung=&spielerposition_id=&altersklasse=&leihe=&w_s=&plus=1&page={r}'
    RequisicaoPagina = requests.get(pagina, headers=headers)
    RaspagemPagina = BeautifulSoup(RequisicaoPagina.text, 'html.parser')

    body = RaspagemPagina.find_all("tr", {'class': 'odd'})
    for i in body:
        ListaJogadores.append(str(i).split('<img alt="')[
            1].split('class')[0][0:-2])
        Posicao = str(i).split('<td')[5]
        Posicao = re.sub("^[>]|(</td></tr></table></td>)", "", Posicao)
        ListaPosicao.append(Posicao)
        ListaIdade.append(str(i).split('class="zentriert">')
                          [2].split('</td>')[0])
        ListaNacionalidade.append(str(i).split('<img alt="')[
            2].split('class')[0][0:-2])
        ListaValor.append(str(i).split('a href="')[
                          4].split('>')[1].split('<')[0])

final_arquivo = pd.DataFrame({"Nome Jogador": ListaJogadores,
                              "Idade": ListaIdade,
                              "Posição": ListaPosicao,
                              "Nacionalidade": ListaNacionalidade,
                              "Valor": ListaValor
                              })
final_arquivo.to_excel(
    r"I:\PythonResquet\Planilha\JogadoresVasco.xlsx", index=False)
