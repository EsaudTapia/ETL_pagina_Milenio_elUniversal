from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from flask import request
from common import config

#Generalizamos a una clase para representar cualquier página de noticias
class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None

        self._visit(url)

#Método para ejecutar una consulta en el árbol html
    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        #Definimos la cabeceras de la petición
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = Request(url, headers=hdr)
        #Abrimos la página
        response = urlopen(request)
        #Creamos el objto BeautifulSoup
        self._html = BeautifulSoup(response.read(), 'html.parser')

#Creamos una clase que representa la página princpal
class HomePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)
        
        #Retornamos la lista evitando repetidos
        return set(link['href'] for link in link_list)
    
#Creamos una clase que representa la página con la información del artículo con base en NewsPage
class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        self._url = url
        super().__init__(news_site_uid, url)
     
    #Definimos una propiedad que contiene el cuerpo del artítulo   
    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''
    
    #Definimos una propiedad que contiene el título del artítulo   
    @property
    def title(self):
        result = self._select(self._queries['article-title'])
        return result[0].text if len(result) else ''
    
    #Definimos una propiedad que contiene la url del artítulo   
    @property
    def url(self):
        return self._url