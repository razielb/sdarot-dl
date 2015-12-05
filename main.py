#!/usr/bin/env python
import urllib2
import urllib
import socket
import re
import json
from os import system

"""
	Coded by R4z
	Email: raziel.b7@gmail.com
"""

class Sdarot(object):

	anal = False
	cookie = ""
	def download_season(self, serie, season):
		data = "episodeList=true&serie=%s&season=%s" % (serie, season)
		# data = "watch=true&serie=53&season=1&episode=10"
		http = { "Accept" : "application/json,text/javascript,*/*; q=0.01",
			"Accept-Encoding" : "",
			"Accept-Language" : "he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4",
			"Connection" : "keep-alive",
			"Content-Length" : str(len(data)),
			"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
			"Cookie" : "jwplayer.volume=100; %s" % self.cookie,
			"Host" : "www.sdarot.tv",
			"Origin" : "http://www.sdarot.tv",
			"Referer" : "http://www.sdarot.tv/watch/53-%D7%90%D7%99%D7%9A-%D7%A4%D7%92%D7%A9%D7%AA%D7%99-%D7%90%D7%AA-%D7%90%D7%9E%D7%90-how-i-met-your-mother/season/1/episode/10",
			"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
			"X-Requested-With" : "XMLHttpRequest"
		}
		opener = urllib2.build_opener()
		req = urllib2.Request("http://www.sdarot.tv/ajax/watch", data, http)
		res = opener.open(req)
		html = json.loads(res.read())
		res.close()
		for episode in html:
			print episode["episode"]
			self.download_episode(serie, season, int(episode["episode"]))
		# print html
	def download_episode(self, serie, season, episode):
		data = "watch=false&serie=%d&season=%d&episode=%d" % (serie, season, episode)
		# data = "watch=true&serie=53&season=1&episode=10"
		http = { "Accept" : "application/json,text/javascript,*/*; q=0.01",
			"Accept-Encoding" : "",
			"Accept-Language" : "he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4",
			"Connection" : "keep-alive",
			"Content-Length" : str(len(data)),
			"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
			"Cookie" : "jwplayer.volume=100; %s" % self.cookie,
			"Host" : "www.sdarot.tv",
			"Origin" : "http://www.sdarot.tv",
			"Referer" : "http://www.sdarot.tv/watch/53-%D7%90%D7%99%D7%9A-%D7%A4%D7%92%D7%A9%D7%AA%D7%99-%D7%90%D7%AA-%D7%90%D7%9E%D7%90-how-i-met-your-mother/season/1/episode/10",
			"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
			"X-Requested-With" : "XMLHttpRequest"
		}
		opener = urllib2.build_opener()
		req = urllib2.Request("http://www.sdarot.tv/ajax/watch", data, http)
		res = opener.open(req)
		html = json.loads(res.read())
		res.close()
		d = html.has_key("error")
		if d == True:
			print "Sharmotot"
			self.download_episode(serie, season, episode)
		else:
			print html
			download_url = "http://%s/watch/sd/%s.mp4?token=%s&time=%d" % (html["url"], html["VID"], html["watch"]["sd"], html["time"])
			print download_url
			from time import sleep
			sleep(3)
			# self.download(download_url, "%s-%s-%s.mp4" % (serie, season, episode))
	def download(self, url, file_name): # http://stackoverflow.com/a/22776
		u = urllib2.urlopen(url)
		f = open(file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])

		file_size_dl = 0
		block_sz = 8192
		while True:
			print "Downloading: %s Bytes: %s" % (file_name, file_size)
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status
			system("cls")
	def server_status(self):
	
		x = urllib2.urlopen("http://www.sdarot.tv/status")
		data = x.read()
		x.close()
		servers = re.findall('<div class="ts">\n\t\t\t\t\t<div class="pb">\n\t\t\t\t\t\t<div class="out">\n\t\t\t\t\t\t\t<div class="p">(.*?)%</div>\n\t\t\t\t\t\t\t<div class="in" style="width: .*?%;"></div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t<h2>.*?([0-9]{1})</h2>\n\t\t\t\t</div>', data)
		for server in servers:
			if float(server[0]) < 100.00: # Check if any server is available
				self.anal = True
				break
		print servers
		return self.anal
	

if __name__ == '__main__':
	s = Sdarot()
	s.server_status()
	# print s.download_episode(88, 5, 9)
	# s.download_episode(53,9,15)
	# print s.download_season(53, 1)
