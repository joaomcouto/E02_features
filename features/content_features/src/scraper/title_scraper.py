import json
import os
import statistics
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from newspaper import Article


def get_title(url):
    """
    Using newspaper3k receives
    a url and capetures it's title
    """
    try:
        # Faz a busca utilizando newspaper3k
        article = Article(url, language='pt')
        article.download()
        article.parse()
    except:
        print("__uso selenium")
        # Faz a busca utilizando selenium
        article = Article(url, language='pt')
        article.html = __get_html_with_selenium(url)
        article.download_state = 2
    article.parse()

    return article.title


def __get_html_with_selenium(url):
    # Set Chrome options:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    # Create drive:
    driver_dir = os.environ.get('CHROME') #'./scraper/resources/chromedriver'#
    driver = webdriver.Chrome(options=chrome_options,executable_path=driver_dir)
    # Specify wait time:
    wait = WebDriverWait(driver, 15)
    # Access url:
    driver.get(url)
    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body"))
        )
    time.sleep(3)
    # return HTMl:
    return driver.page_source

def extract_title(s):
    filters = ['.html', '.aspx', '.ghtml', 'html','.']
    parse = s.split('/')
    for el in reversed(parse):
        if '-' in el:
            if any(x in el for x in filters):
                return el.split('.')[0].replace('-',' ')
            return el.replace('-',' ')
    return 'NULL'
    
def get_title_url(url):
    print('__tituloURL')
    filters = ['.google','/render','/social_annotation','/start','pagina-','.jpeg','fato-ou-fake','.bmp','.png','.pdf'] 
    if any(s in url for s in filters):
        return 'NULL'
    title = extract_title(url)
    return title


def execute(source,url):
    source_parse = source.split('.')
    source_name = source_parse[1].upper() if source_parse[0].upper == 'WWW' else source_parse[0].upper()
    filters_url = ['OPS','404','NOT FOUND','EXCESSIVE TRAFFIC', 'SERVER ERROR','N??O ENCONTRADA',
    'ERROR','CONTEUDO INDISPONIVEL','PLEASE WAIT','COMENT??RIO, NOT??CIAS E COMPORTAMENTO','Igreja, vida crist??, opini??o e estudos b??blicos'
    'SURVEY IS CLOSED','Portal de not??cias gospel.',' Tudo o que acontece em Tocantins e regi??o','A sua fonte segura de informa????o',
    'F??, pol??tica e cosmovis??o crist??','Infowars:','a War on For Your Mind!','vida crist??']

    filters_null = ['jornal regional','pagina-','Not??cias de Dourados-MS e regi??o','Conte??do de Tecnologia do UOL','#fato ','#fake ',
     'jornal do dia']
    
    filters_null = [i.upper() for i in filters_null]
    filters_url = [i.upper() for i in filters_url]
    
    if 'HTTPS://'+source.upper()+'/' == url.upper():
        return 'NULL'
    try:
        title = get_title(url)
    except:
        print('__exce????o')
        return get_title_url(url)

    if any(x in title.upper() for x in filters_null) or len(title.split(' ')) <= 2:
        return 'NULL'

    if any(x in title.upper() for x in filters_url):
        print('_filtro ',title)
        title = get_title_url(url)

    return title





def lendo_dataset(localizacao_arquivo):
    """
    Reads MP dataset
    """
    dados = []
    with open(localizacao_arquivo, mode='r') as f:
        for line in f:
            dados.append(json.loads(line.strip()))
    return dados



def teste():
    data = lendo_dataset('./scraper/dados/testes/DATASET_MPMG-FakeNews_matched.txt')#'./data/DATASET_MPMG-FakeNews_matched.txt')
    scrape_times = []
    equal_cnt = 0
    contained_cnt = 0
    different_cnt = 0

    for news in data:
        url = news['url']
        original_title = news['title'].strip()
        start_article = time.time()
        try:
            scraped_title = get_title(url).strip()
        except:
            print("\n---PROB: ", url)
            print("\n")
            continue
        end_article = time.time()
        scrape_times.append(end_article - start_article)
        print("TIME: ", end_article - start_article)
        print("ORIGIINAL:\n", original_title)
        print("SCRAPED:\n", scraped_title)
        if scraped_title == original_title:
            equal_cnt += 1
        elif scraped_title in original_title:
            contained_cnt += 1
        else:
            different_cnt += 1
            print("---DIF: ", url)
        print()
    print("\n----------")
    print("RESULTS FOR TITLES:")
    print("Average time for consult: ", statistics.mean(scrape_times))
    print("Number of equal: ", equal_cnt)
    print("Number of contained: ", contained_cnt)
    print("Number of different: ", different_cnt)

# _s = 'http://events.r20.constantcontact.com/register/event'
# print('\nresultado extra????o: ',extract_title(_s))
# print('titulo: ', get_title_url(_s))