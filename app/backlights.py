import sys
import urllib.request
from xml.dom.minidom import parseString
import time
import psycopg2

#--*-- coding: utf-8 --*--
import urllib.request
from xml.dom.minidom import parseString

class ya_search:
    def __init__(self,query,region='213',page='100'):
        self.query=query
        self.region=region
        self.page=page
    ya_user='kl.bazarov@gmail.com'
    ya_key='688c05a0a9c347b99c960a6d5792eea2'
    
    #ya_user='reactstudio'
    #ya_key='03.513174037:5f1f2bd9e6e8f8f93b10e65aa3d147fb'
    #ya_user='nlp-marketing'
    #ya_key='03.63209051:ee66402f83ea55f2ba77bb1ad4a1d19c'
    
    def yandex_key(self):
        return ('https://xmlproxy.ru/search/xml?user='+self.ya_user+'&key='+self.ya_key+'&lr=')
    def xml_build(self):
        defaults_xml='''<?xml version="1.0" encoding="UTF-8"?>
            <request>
            <query>%s</query>
            <groupings>
            <groupby attr="d" mode="deep" groups-on-page="%s"  docs-in-group="1" />
            </groupings>
            </request>'''
        return (defaults_xml % (self.query,self.page)).encode()
    def response(self):
        ya_url=self.yandex_key()+self.region
        return (urllib.request.urlopen(ya_url,self.xml_build())).read().decode()
    def urls(self, url_counts):
        urls_xml=[]
        dom_xml=parseString(self.response()).getElementsByTagName('url')
        for node in dom_xml:
            urls_xml.append(node.childNodes[0].nodeValue.lower())
        return urls_xml[:url_counts]

    def parse(self,url):
        i=0
        xml_urls=self.urls(10)
        #print(xml_urls)
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

def go_go(response_object):

#    test = ya_search()
#    res = test.parse("https://www.eskimoscow.ru/")

#    domain = 'https://www.eskimoscow.ru/'
#    project = 'йоооо'
#    query_lst = ['ремонт холодильников']

#    con = psycopg2.connect(dbname='seohack', user='seohack', 
#                            password='my_password', host='localhost')
#    print("Database opened successfully")
#    cur = con.cursor()
    res2 = dict()
#    curr_data = time.strftime('%x')
    for i in response_object['keys']:
        test = ya_search(i)
        res2[i] = test.urls(response_object['depth'])
#        res = test.parse(domain)
#        print(res)
#        res2.append((project, domain, i, res[0], res[1], curr_data))
#        cur.execute("INSERT INTO seohacks_positions (project, domain, phrase, phrase_position, url_position, data_position) VALUES (%s, %s, %s, %s, %s, %s)", (project, domain, i, res[0], res[1], curr_data))
#    con.commit()
#    print("Record inserted successfully")  

#    con.close()
    print(res2)
    return res2