import urllib.request, urllib.parse
from xml.dom.minidom import parseString
import requests

class ya_search_xmlriver:
    def __init__(self, query, loc, groupby, lr, domain, country, device):
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
#        groupby – числовое значение, ТОП позиций для сбора. Возможные значения: 10, 20, 30, 50, 100;
#        loc – числовое значение (id) местоположения из этого файла;
#        country – числовое значание (id) страны из этого файла;
#        lr – код языка из файла языков;
#        domain – числовое значение (id) google домена из этого файла;
#        device – устройство (desktop, tablet, mobile).
        
    def yandex_key(self):
        return '{0}{1}&key={2}&query={3}&loc={4}&groupby={5}&lr={6}&domain={7}&country={8}&device={9}'.format(self.base_url, self.ya_user, self.ya_key, urllib.parse.quote_plus(self.query), self.loc, self.groupby, self.lr, self.domain, self.country, self.device)
    
    def response(self):
        ya_url=self.yandex_key()
        return (urllib.request.urlopen(ya_url)).read().decode()
    
    def urls(self, groupby):
        urls_xml=[]
        dom_xml=parseString(self.response()).getElementsByTagName('url')
        for node in dom_xml:
            urls_xml.append(node.childNodes[0].nodeValue.lower())
        return urls_xml[:groupby]
    
    def parse(self,url):
        i=0
        xml_urls=self.urls()
        while i<len(xml_urls):
            if url in xml_urls[i]:
                break
            i += 1
        if i+1<len(xml_urls):
            return i+1,xml_urls[i]
        else:
            return 0, 'Нет в топ 100'
        
    def parse2(self,url):
        xml_urls=self.urls()
        results=[x for x in xml_urls if url in x ]
        try:
            return (xml_urls.index(results[0])+1,results[0])
        except:
            return 0, 'Нет в топ 100'