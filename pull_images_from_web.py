#!/usr/bin/env python
# encoding: utf-8

import requests
from pyquery import PyQuery as pq
import urllib
import argparse
import sys
import os

BASE_URL = 'http://mugshots-directory.com'

try:
	os.mkdir('mugshots')
except:
	pass

CURL_COMMAND = "curl %s -o mugshots/%s"


def write_image_to_file(image_url, image_name):
	with open(image_name, 'wb') as handle:
		request = requests.get(image_url, stream=True)

		for block in request.iter_content(1024):
			if not block:
				break
			handle.write(block)
		print 'image ===> ', image_name
	return image_name


def pull_images_from_web(options):
	
	def _get_url(url):
		print '---> ', url
		d = pq(url=url,opener=lambda url, **kw: urllib.urlopen(url).read())
		index = 0
		for e in d(".persons img").items():
			try:
				image_src  = str(e.attr.src)
				if image_src and 'noimg' not in image_src:
					image_name = "mugshots/%s" % image_src.split("/")[len(image_src.split("/"))-1]
					image_src = "%s%s" % (BASE_URL,image_src)
					#command = CURL_COMMAND % (image_src,image_name)
					#os.system(CURL_COMMAND % (image_src,image_name))
					write_image_to_file(image_src,image_name)

			except Exception, exc:
				print "ERROR: %s" % str(exc)
	
	if not options.page:
		for page in range(options.start,options.end+1):
			url = 'http://mugshots-directory.com/page/%s' % page
			_get_url(url)
	else:
		url = 'http://mugshots-directory.com/page/%s' % options.page
		_get_url(url)
		


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--page', dest='page', type=int, default=None)
	parser.add_argument('--start', dest='start', type=int, default=None)
	parser.add_argument('--end', dest='end', type=int, default=None)
	
	sys.exit(pull_images_from_web(parser.parse_args()))
	

