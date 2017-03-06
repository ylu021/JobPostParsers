import sys
import urllib
import re
import time 
import json
from flask import render_template_string
from bs4 import BeautifulSoup

def generate(url, start):
    domain = 'https://www.indeed.com'
    while url:
        content = urllib.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        alllink = soup.find_all('a')
        for link in alllink:
            if 'rel' in link.attrs and 'nofollow' in link['rel']:
                if re.match('/rc/clk.*?',link.get('href')):
                    obj = {}
                    obj['link'] = domain+str(link.get('href'))
                    obj['name'] = link.text.encode('utf-8').replace(',', '-')
                    # template = '<li><a href="{{ link }}">{{ name }}</a></li>'
                    # yield render_template_string(template, **obj)
                    yield obj
                    time.sleep(1)

        url = None
        div = soup.find('div', class_="pagination")
        # print(div)
        link = div.find_all('a')[-1]
        if link.text and 'next' in link.text.lower():
            url = domain+str(link.get('href'))
            generate(url, start+10)
        
    
