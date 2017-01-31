import sys

def find_job(url):
    dic = {}
    indeed_parse(dic, url, 0)

def indeed_parse(dic, url, start):
        import urllib
        import re
	from bs4 import BeautifulSoup
	domain = 'https://www.indeed.com'
	content = urllib.urlopen(url).read()
	soup = BeautifulSoup(content, 'html.parser')
        alllink = soup.find_all('a')

        for link in alllink:
            if 'rel' in link.attrs and 'nofollow' in link['rel']:
                if re.match('/rc/clk.*?',link.get('href')) and link.get('href') not in dic.values():
                    dic[link.text.encode('utf-8').replace(',','-')] = domain+str(link.get('href'))
                    mydiv = re.match("<a href='"+url+"&start="+str(start)+"&pp=.+>'", content)
        alldiv = soup.find_all('div')

        mydiv = None
        for d in alldiv:
            if 'class' in d.attrs and 'pagination' in d['class']:
                mydiv = d.find_all('a')[-1]

        if 'next' in mydiv.text.lower():
            url = domain+str(mydiv.get('href'))
            print url#feel free to print out url to see progress
            indeed_parse(dic, url, start+10)
        
        with open('job_results.csv', 'w') as f:
            [f.write('{0},{1}\n'.format(key, value)) for key, value in dic.items()]
        return dic

