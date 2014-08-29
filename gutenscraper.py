import sys

from bs4 import BeautifulSoup
import requests

def _scrape_html_book_content(base_url, book_rel_url, headers):
	# book_rel_url is of the form '/ebooks/12701'
	# html urls of the books look like 'http://www.gutenberg.org/files/12701/12701-h/12701-h.htm'
	book_id = book_rel_url.split('/')[-1]
	html_url = '{}/files/{}/{}-h/{}-h.htm'.format(base_url, book_id, book_id, book_id)

	r = requests.get(plain_text_url, headers=headers)
	soup = BeautifulSoup(r.content)

	# For testing use some local files to avoid being blocked (too lazy for header spoofing...)
	#ff = open('/Users/thomas/DevSandbox/InfiniteSandbox/gutenscraper/verwandlung.html', 'r')
	#soup = BeautifulSoup(ff.read())
	#ff.close()

	# TODO:	Still leaves a few tags and some other stuff in the content, but good enough for now
	# 		Or in other words "Ain't no Tom Penny, but [it] will do!"
	paragraphs = soup.findAll('p')
	content = map(lambda tag: tag.contents[0], paragraphs)

	return content

def search_books(search_term, base_url='http://www.gutenberg.org', headers=None):
	params = {'query': search_term}

	req_url = '{}{}'.format(base_url, '/ebooks/search/')

	r = requests.get(req_url, params=params, headers=headers);
	soup = BeautifulSoup(r.content)

	# Local Dev, Local Files
	#f = open('/Users/thomas/DevSandbox/InfiniteSandbox/gutenscraper/search_result.html', 'r')
	#soup = BeautifulSoup(f.read())
	#f.close()

	search_results = soup.findAll('li', {'class': 'booklink'})

	books = list()

	for result in search_results:
		book = dict()

		book['url'] = '{}{}'.format(base_url, result.a['href'])
		book['content'] = _scrape_html_book_content(base_url, result.a['href'], headers)

		temp_result = result.findAll('span', {'class': 'title'})
		book['title'] = temp_result[0].contents[0]

		temp_result = result.findAll('span', {'class': 'subtitle'})
		book['author'] = temp_result[0].contents[0]

		books.append(book)

	return books

if (__name__ == '__main__'):
	search_books(sys.argv[1] if len(sys.argv) > 1 else 'kafka')
