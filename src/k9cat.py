#!/usr/bin/env python
#
# webcat.py - URL categorization script
#
# Author: Xavier Mertens <xavier@rootshell.be>
# Copyright: GPLv3 (http://gplv3.fsf.org)
# Fell free to use the code, but please share the changes you've made
#
# Todo
# - Add proxy support
#

import os
import sys
import stat
import argparse
import errno
import urllib2
import json
import time
import ast
from xml.etree.cElementTree import fromstring
from json import dumps

class K9Cat( object ):
	def __init__( self, k9license ):

		# Configuration
		self.categoriesFile = '/var/tmp/categories.txt'
		self.categoriesUrl = 'http://sitereview.bluecoat.com/rest/categoryList?alpha=true'

		# Get one here: http://www1.k9webprotection.com/get-k9-web-protection-free
		self.k9License = k9license

	def fetchCategories(self, name):
		""" --------------------------------------- """
		""" Fetch categories and create local cache """
		""" --------------------------------------- """
		if not name:
			return None

		try:
			u = urllib2.build_opener()
			u.addheaders = [('User-agent', 'webcat.py/1.0 (https://blog.rootshell.be)')]
			r = u.open(self.categoriesUrl)
			data = json.load(r)
			d = dict([('%02x' % c['num'], c['name']) for c in data])
		except urllib2.HTTPError, e:
			sys.stderr.write('Cannot fetch categories, HTTP error: %s\n' % str(e.code))
		except urllib2.URLError, e:
			sys.stderr.write('Cannot fetch categories, URL error: %s\n' % str(e.reason))
		try:
			f = open(name, 'wb')
			f.write(dumps(d))
		except Exception, e:
			f.close()
			sys.stderr.write('Cannot save categories: %s\n' % e)
		return d

	def loadCategories(self, name):
		""" --------------------------------- """
		""" Load categories from a cache file """
		""" --------------------------------- """
		if not name:
			return None
		d = {}
		try:
			f = open(name, 'r')
			data = f.read()
			d = ast.literal_eval(data)
		
		except Exception, e:
			f.close()
			sys.stderr.write('Cannot load categories: %s (use -F for force a fetch)\n' % e)
			exit(1)
		return d

	def _chunks(self, s):
		# Original: https://github.com/allfro/sploitego/blob/master/src/sploitego/webtools/bluecoat.py
		return [s[i:i + 2] for i in range(0, len(s), 2)]

	def CheckCat( self, hostname, force=False): 	
		hostname = hostname.rstrip()	
		category = "Uncategorized"
		if not os.path.exists(self.categoriesFile) or \
			(time.time() - os.stat(self.categoriesFile)[stat.ST_MTIME]) > 7200 or force:
			webCats = self.fetchCategories(self.categoriesFile)
		else:
			webCats = self.loadCategories(self.categoriesFile)

		r = urllib2.urlopen('http://sp.cwfservice.net/1/R/%s/K9-00006/0/GET/HTTP/%s/%s///' % (self.k9License, hostname, 80))
		if r.code == 200:
			e = fromstring(r.read())
			domc = e.find('DomC')
			dirc = e.find('DirC')
			if domc is not None:
				cats = self._chunks(domc.text)
				category = webCats.get(cats[0].lower())
			elif dirc is not None:
				cats = self._chunks(dirc.text)
				category = webCats.get(cats[0].lower())

		return category	
