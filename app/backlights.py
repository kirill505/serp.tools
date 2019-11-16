import urllib.request, urllib.parse
from xml.dom.minidom import parseString
import requests

from lxml import html

class ya_search_xmlriver:
    def __init__(self, query, loc, groupby, lr, domain, country, device, delayed=1):
        self.base_url = 'http://xmlriver.com/search/xml?user='
        self.ya_user = '798'
        self.ya_key='c17a38a762f9f72d80d12489ee7b5d4b35dd2aff'
        self.query = query
        self.loc = loc
        self.groupby = groupby
        self.lr = lr
        self.domain = domain
        self.country = country
        self.device = device
        self.delayed = delayed
#        groupby – числовое значение, ТОП позиций для сбора. Возможные значения: 10, 20, 30, 50, 100;
#        loc – числовое значение (id) местоположения из этого файла;
#        country – числовое значание (id) страны из этого файла;
#        lr – код языка из файла языков;
#        domain – числовое значение (id) google домена из этого файла;
#        device – устройство (desktop, tablet, mobile).
        
    def get_url_delayed_response(self):
        return '{0}{1}&key={2}&query={3}&loc={4}&groupby={5}&lr={6}&domain={7}&country={8}&device={9}&delayed={10}'.format(self.base_url, self.ya_user, self.ya_key, urllib.parse.quote_plus(self.query), self.loc, self.groupby, self.lr, self.domain, self.country, self.device, self.delayed)
    
    def get_response_in_xmlriver(url):
        
        return (urllib.request.urlopen(url)).read().decode()

    def get_urls_in_xmlriver(url):
        response = get_response_in_xmlriver(url)

        urls_xml=[]
        dom_xml=parseString(response.getElementsByTagName('url'))
        for node in dom_xml:
            urls_xml.append(node.childNodes[0].nodeValue.lower())
        return urls_xml