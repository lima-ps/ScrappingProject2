import pip._vendor.requests as requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#config
topics_url = 'https://github.com/topics'
resp = requests.get(topics_url) #obtem a pagina
content = resp.text #converte para string
doc = bs(content, 'html.parser')

#cria um ficheiro html com atribuição de escrita e insere nesse ficheiro o texto obtido da nossa url
with open('webpage.html', 'w', encoding="utf-8") as f:
    f.write(content)

#encontrando os elementos pretendidos

topics = doc.find_all('p', {'class':'f3 lh-condensed mb-0 mt-1 Link--primary'})
descriptions = doc.find_all('p', {'class':'f5 color-fg-muted mb-0 mt-1'})
topics_link = doc.find_all('a', {'class':'no-underline flex-1 d-flex flex-column'})


#salvando os elementos em listas
topics_list = []
for top in topics:
    topics_list.append(top.text)

descriptions_list = []
for desc in descriptions:
    descriptions_list.append(desc.text.strip())

links_list = []
for link in topics_link:
    links_list.append('https://github.com/topics'+link['href'])

#criando nossa tabela
topics_dict = {
    'Title':topics_list,
    'Description':descriptions_list,
    'URLs':links_list
}
topic_df = pd.DataFrame(topics_dict)
topic_df

#Salvando em CSV
topic_df.to_csv('topics.csv', index=None)

'''-------------------- página2: detalhes dos tópicos--------------'''

