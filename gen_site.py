from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from functools import reduce
from duckduckgo_search import DDGS
import datetime


link = 'http://www.90minut.pl/liga/1/liga13482.html'

tabela, tabela_linki = [], []

response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')

soup = (soup.find('table', class_ = 'main2'))


def write_layout(file, title):
    file.write(f'---\nlayout: page\ntitle: {title}\n---\n')


# Tylko aktualizacja tabeli.
with open('tabela.md', 'w') as f:
    write_layout(f, "Tabela, stan na " + datetime.datetime.now().strftime("%x"))
    for pozycja, dane in enumerate(soup.find_all('td', align='left')[1:]):
        
        a = dane.find('a')
        tabela.append(a.string)
        tabela_linki.append((reduce(lambda x,y: x + '_' + y, unidecode(a.string).split())).lower())
        
        s = '# ' + str((pozycja + 1)) + '. ' + a.string + '\n'
        t = f"  * [Dodatkowe informacje](http://www.90minut.pl{a['href']})\n"
        v = f"  * [Wyniki z duckduckgo]({{{{ '/tabela/{tabela_linki[-1]}' | relative_url }}}})\n\n" 
   
        f.write(s)
        f.write(t)
        f.write(v)



# Generowanie całej strony.
for i in range(len(tabela)):
    with open(f'tabela/{tabela_linki[i]}.md', 'w') as f:
        
        write_layout(f, f'{tabela[i]} - wyniki z DuckDuckGo')
        info = DDGS().text(keywords=tabela[i], region="pl-pl", safesearch="off", timelimit="m", max_results=3)
        f.write(f'# {tabela[i]} - informacje.\n')
        for j in info:
            f.write(f"  * {j['body']}, [Cały artykuł]({j['href']}).\n")

        herb = DDGS().images(keywords=f'{tabela[i]} + herb',region="pl-pl",safesearch="off",size=None,type_image=None,layout=None,license_image=None,max_results=1)
        stadion = DDGS().images(keywords=f'{tabela[i]} + stadion',region="pl-pl",safesearch="off",size=None,type_image=None,layout=None,license_image=None,max_results=1)
        herb_data = requests.get(herb[0]['image']).content
        stadion_data = requests.get(stadion[0]['image']).content
        with open(f'tabela/{tabela_linki[i]}_herb.jpg', 'wb') as pic:
            pic.write(herb_data)
        with open(f'tabela/{tabela_linki[i]}_stadion.jpg', 'wb') as pic:
            pic.write(stadion_data)
        
        f.write(f'\n\n# {tabela[i]} - herb\n')
        f.write(f'  ![herb]({tabela_linki[i]}_herb.jpg)\n\n')
        f.write(f'# {tabela[i]} - stadion\n')
        f.write(f'  ![stadion]({tabela_linki[i]}_stadion.jpg)') 
        
