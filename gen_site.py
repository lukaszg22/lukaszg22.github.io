from bs4 import BeautifulSoup
import requests
import os
import markdown as md
from unidecode import unidecode
from functools import reduce
from duckduckgo_search import DDGS


link = 'http://www.90minut.pl/liga/1/liga13482.html'

tabela, tabela_linki = [], []

response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')
# W tabeli z klasą main2 znajduje się tabela.
soup = (soup.find('table', class_ = 'main2'))
# W td ustawionych do lewej, poza pierwszym, znajdują się nazwy kolejnych drużyn.

def write_layout(file):
    file.write('---\nlayout: page\n---\n')

with open('tabela.md', 'w') as f:
    write_layout(f)
    for pozycja, dane in enumerate(soup.find_all('td', align='left')[1:]):
        
        a = dane.find('a')
        #print(str(pozycja + 1) + ".", a.string, a['href'])
        tabela.append(a.string)
        tabela_linki.append((reduce(lambda x,y: x + '_' + y, unidecode(a.string).split())).lower())
        
        s = '# ' + str((pozycja + 1)) + '. ' + a.string + '\n'
        t = '  * [Dodatkowe informacje](http://www.90minut.pl/skarb.php?id_klub=132&id_sezon=105)\n'
        v = f'  * [Wyniki z duckduckgo]({tabela_linki[-1]})\n\n'
            
        f.write(s)
        f.write(t)
        f.write(v)


        

for i in range(len(tabela)):
    with open(f'tabela/{tabela_linki[i]}.md', 'w') as f:
        write_layout(f)
        info = DDGS().text(keywords=tabela[i], region="pl-pl", safesearch="off", timelimit="m", max_results=3)
        f.write(f'# {tabela[i]} - informacje.\n')
        for j in info:
            f.write(f"  * {j['body']}, [Cały artykuł]({j['href']}).\n")
    break




