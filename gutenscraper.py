import sys

from bs4 import BeautifulSoup
import requests

def _scrape_plain_text_content(base_url, book_rel_url, headers):
	# book_rel_url is of the form '/ebooks/12701'
	# plain text urls look like 'http://www.gutenberg.org/cache/epub/12701/pg12701.txt'
	book_id = book_rel_url.split('/')[-1]
	plain_text_url = '{}/cache/epub/{}/pg{}.txt'.format(base_url, book_id, book_id)

	r = requests.get(plain_text_url, headers=headers)

	#ff = open('/Users/thomas/DevSandbox/InfiniteSandbox/gutenscraper/pg12701.txt', 'r')

	# The actual book content contains lots of rubbish like license information and other stuff
	# Start of the book is usually marked with '***START OF THE PROJECT GUTENBERG EBOOK <BOOK TITLE>***'
	# The end of the book is makred with '***END OF THE PROJECT GUTENBERG EBOOK <BOOK TITLE>***'
	book_content = r.content
	#book_content = ff.read()
	#ff.close()

	book_prefix_primary = '***START OF THE PROJECT'
	book_prefix_secondary = '***'
	book_suffix = '***END OF THE PROJECT'

	start = book_content.find(book_prefix_primary)
	book_content = book_content[start + len(book_prefix_primary):]
	start = book_content.find(book_prefix_secondary)
	end = book_content.rfind(book_suffix)

	return book_content[start + len(book_prefix_secondary):end].strip()

def search_books(search_term, base_url='http://www.gutenberg.org', headers=None):
	params = {'query': search_term}

	req_url = '{}{}'.format(base_url, '/ebooks/search/')

	r = requests.get(req_url, params=params, headers=headers);

	soup = BeautifulSoup(r.content)
	#f = open('/Users/thomas/DevSandbox/InfiniteSandbox/gutenscraper/dump.html', 'r')
	#soup = BeautifulSoup(f.read())

	search_results = soup.findAll('li', {'class': 'booklink'})

	books = list()

	for result in search_results:
		book = dict()

		book['url'] = '{}{}'.format(base_url, result.a['href'])
		book['content'] = _scrape_plain_text_content(base_url, result.a['href'], headers)

		temp_result = result.findAll('span', {'class': 'title'})
		book['title'] = temp_result[0].contents[0]

		temp_result = result.findAll('span', {'class': 'subtitle'})
		book['author'] = temp_result[0].contents[0]

		print 'TITLE:', book['title']

		books.append(book)


	for book in books:
		print 'AUTHOR=%s, TITLE=%s' % (book['author'], book['title'])
		print 'CONTENT:', book['content'][:100]

	return books

if (__name__ == '__main__'):
	search_books(sys.argv[1] if len(sys.argv) > 1 else 'kafka')
