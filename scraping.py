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
    links_list.append('https://github.com'+link['href'])

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

topics_links = links_list[0]  #recebe as urls das paginas de cada tópico

resp = requests.get(topics_links)
topics_page = bs(resp.text, 'html.parser') #pagina completa
baseurl = 'https://github.com'
stars_tag = topics_page.find_all('span', {'id':"repo-stars-counter-star"})
topics_page_tags = topics_page.find_all('h3', {'class':'f3 color-fg-muted text-normal lh-condensed'}) #pagina com a classe que contem as tags que precisamos


#function para converter a 'star' em numero.
def parse_stars(star_str):
    if star_str[-1] == 'k': #valida se termina com "k"
        return int(float(star_str[:-1]) * 1000) #converte e retorna

# retorna toda a informação necessária de um repositório
def get_info(topics_page_tags, stars_tag):
    topics_page_a_tags = topics_page_tags.find_all('a') #filtra apenas as tags 'a' do 'topics_page_tags'
    username = topics_page_a_tags[0].text.strip()
    reponame = topics_page_a_tags[1].text.strip()
    repolink = baseurl+topics_page_a_tags[1]['href']
    stars = parse_stars(stars_tag.text)
    return username, reponame, stars, repolink

# retorna info de todos os repositorios
def get_topic_repo(links_list):
    response = requests.get(links_list)
    if response.status_code != 200: #check response
        raise Exception('Failed to load page {}'.format(links_list))
    topic_page = bs(response.text, 'html.parser')
    stars_tag = topics_page.find_all('span', {'id':"repo-stars-counter-star"})
    topics_page_tags = topic_page.find_all('h3', {'class':'f3 color-fg-muted text-normal lh-condensed'}) #pagina com a classe que contem as tags que precisamos

#   save de repo
    topic_repo_dict = {
    'username': [],
    'reponame': [],
    'stars': [],
    'repourl': []
    }

    #get repo info
    for i in range(len(topics_page_tags)):
        repo_info = get_info(topics_page_tags[i], stars_tag[i])
        topic_repo_dict['username'].append(repo_info[0])
        topic_repo_dict['reponame'].append(repo_info[1])
        topic_repo_dict['stars'].append(repo_info[2])
        topic_repo_dict['repourl'].append(repo_info[3])

    return pd.DataFrame(topic_repo_dict)


url4 = links_list[4]
teste = get_topic_repo(url4)

