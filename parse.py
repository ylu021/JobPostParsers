def parseParagraphs(url, where):
	from bs4 import BeautifulSoup
	import urllib

	content = urllib.urlopen(url)
	soup = BeautifulSoup(content, 'html.parser').find_all(where)
	tab = soup[1]
	paras = tab.find_all('p')
	indexes = []
	sentences = []
	for i in range(len(paras)):
            "customize in here"
        return indexes, sentences

