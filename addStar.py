#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import simplejson
import sys

# 使う為にはsimplejsonが必要
# aptitude install python-simplejsonとかで入れてください

# Firefox2等ではてなつないだ時のcookieのパスを書いてください
cookies_file ="/Users//cookies.txt"

class SHatena():

	def signIn(self):
		import cookielib

		jar = cookielib.MozillaCookieJar()
		jar.load(cookies_file)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

		return opener

	def __init__(self,dist):
		opener = self.signIn()	
		d = opener.open("http://s.hatena.ne.jp/entries.json")
		data = d.read()
		rks = simplejson.loads(data)["rks"]

		hsAdd = "http://s.hatena.ne.jp/star.add.json?uri="
		url = hsAdd+dist+"&rks="+rks
		data = opener.open(url)
		urlstring = data.read()
		print urlstring

if __name__ == "__main__":
	sh = SHatena(sys.argv[1])
