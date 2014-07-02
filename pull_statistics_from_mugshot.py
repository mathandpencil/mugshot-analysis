#!/usr/bin/env python
# encoding: utf-8

import requests
from pyquery import PyQuery as pq
import urllib
import argparse
import sys
import os
import glob
BASE_URL = 'http://mugshots-directory.com'

def pull_statistics(options):
	
	def _get_page_statistics(url):
		print '---> ', url
		d = pq(url=url,opener=lambda url, **kw: urllib.urlopen(url).read())
		for e in d(".persons a").items():
			absolute_url = "%s%s" % (BASE_URL,str(e.attr.href))
			print absolute_url
			dd = pq(url=absolute_url,opener=lambda url, **kw: urllib.urlopen(url).read())
			for ee in d("tbody").items():
				print ee.html()
	
	if not options.page:
		for page in range(options.start,options.end+1):
			url = 'http://mugshots-directory.com/page/%s' % page
			_get_page_statistics(url)
	else:
		url = 'http://mugshots-directory.com/page/%s' % options.page
		_get_page_statistics(url)
		


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--page', dest='page', type=int, default=None)
	parser.add_argument('--start', dest='start', type=int, default=None)
	parser.add_argument('--end', dest='end', type=int, default=None)
	sys.exit(pull_statistics(parser.parse_args()))
	