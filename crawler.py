#! /usr/bin/python
#
# Recursively download web pages, store them to files, and return information about their relationships
#
# Test case: download and store a number of pages starting from a seed.
# Example:
# python crawler.py http://en.wikipedia.org/wiki/Business_intelligence 100

import pycurl
import urlparse
import os
import StringIO
import re

# Download a single web page via the pycurl package and return its text
def download (url):
	buffer = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, buffer.write)
	c.perform()
	c.close()
	return buffer.getvalue()

href = re.compile(r'''href\s*=\s*["']([^"']+)["']''') # regex to identify href attributes
protocol = re.compile(r'''^([a-zA-Z\-]+:)?//''') #This identifies absolute links(beginning w/ "protocol:" or "//")

# extract relative hrefs of an HTML text
def get_links (text):
	urls = []
	for url in href.findall (text): #iterate matches of the regex
		if protocol.match(url): #Exclude absolute URLs
			continue
		p = url.find ('#') #Remove anchor
		if p >= 0:
			url = url[:p]
		if len(url) == 0: # if URL is only an anchor skip
			continue
		if url in urls: # if URL is already stored skip
			continue
		if '/wiki/' not in url or ':' in url: # if URLs is not in wiki or is a special page skip
			continue
		urls.append (url) # otherwise keep it
	return urls

# recursive BFS page download;
def recursive_download (seed_url, max_pages, file_folder = 'pages'):
   if not os.access(file_folder, os.W_OK): # Create folder if it doesn't exist
		os.mkdir (file_folder)

   # Separate the protocol (scheme) and domain (netloc) part of the URL
   # to rebuild absolute URL from the relative links
   p = urlparse.urlparse (seed_url)
   base = '%s://%s' % (p.scheme, p.netloc)

   queue = [seed_url] #FIFO queue of URLs to be downloaded
   visited = set() #already downloaded URLs
    
   #while there are unvisited URLs and we don't reach the MAX_VISITED
   while len(queue)>0 and len(visited)<max_pages :
     # Pop the top URL
     url = queue[0]
     del queue[0]
     # create filename
     filename = file_folder + '/' + url.replace ('/', '_')
     try:
			# try loading the page from the file
			f = open (filename, 'r')
			text = f.read()
			f.close ()
     except:
			# if the file does not exist, download it
			# and store it onto the file
			text = download(url)
			f = open (filename, 'w')
			f.write (text)
			f.close ()
     # put URL in the visited list
     visited.add (url)
     # Extract the outgoing links
     links = get_links (text)
     absolute_links = [base + url for url in links]
     yield {
			'filename': filename,
			'url': url,
			'links': absolute_links,
			'text': text
     }
     # Yield new entry
     for abs_url in absolute_links:
			if abs_url not in visited and abs_url not in queue:
				queue.append (abs_url)


if __name__ == '__main__':

	import sys

	seed = sys.argv[1]
	n_pages = int(sys.argv[2])

	for page in recursive_download (seed, n_pages):
		sys.stdout.write ('Page %s:\n\tFilename: %s\n\t%d relative links\n' % (page['url'], page['filename'], len(page['links'])))
