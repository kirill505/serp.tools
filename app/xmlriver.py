from lxml import html
import requests

import urllib.request, urllib.parse
from xml.dom.minidom import parseString

def get_xmlriver_task_response(url, **kwargs):
  response = requests.get(url, params = kwargs)
  tree = html.document_fromstring(response.content)
  
  status = tree.xpath('//status')
  error = tree.xpath('//error')

  #return Result, TaskID, Error
  if tree.xpath('//req_id'):
    task_url = "http://xmlriver.com/search/xml?req_id=" + str(tree.xpath('//req_id')[0].text)
    print(task_url)
    return "SUCCESS", task_url, None
  else:
    return status[0].text, None, error[0].text
       
def get_urls_in_xmlriver(base_url, **kwargs):
    response = requests.get(base_url, params = kwargs)
    
    tree = html.document_fromstring(response.content)
    print(tree.text)
    
    return [i.text for i in tree.xpath('//grouping//group//doc/url')]
      

#url = "http://xmlriver.com/search/xml?user=798&key=c17a38a762f9f72d80d12489ee7b5d4b35dd2aff&query=%D0%BF%D0%B8%D1%86%D1%86%D0%B0&delayed=1"
#url2 = "http://xmlriver.com/search/xml?req_id=270720"
#print(get_xmlriver_task_response(url)[1])

#base_url = 'http://xmlriver.com/search/xml?user=798&key=c17a38a762f9f72d80d12489ee7b5d4b35dd2aff'

#print(get_url_delayed_response(base_url, query = 'доставка пиццы', loc = '1011969'))
#print(get_urls_in_xmlriver("http://xmlriver.com/search/xml?req_id=2841004"))