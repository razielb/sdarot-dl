#!/usr/bin/env python2

import urllib2
import json
import time

'''	coded by R4z		[raziel.b7@gmail.com]
	enhanced by elicn
'''

class Sdarot:

	_HEADERS = {'Cookie'			: r'jwplayer.volume=100;',
				'Referer'			: r'http://www.sdarot.tv/watch/53-%D7%90%D7%99%D7%9A-%D7%A4%D7%92%D7%A9%D7%AA%D7%99-%D7%90%D7%AA-%D7%90%D7%9E%D7%90-how-i-met-your-mother/season/1/episode/10',
				'User-Agent'		: r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36',
				'X-Requested-With'	: r'XMLHttpRequest'}
	_BUFFER_SIZE = (32 * 1024)

	@staticmethod
	def _request_page(serie, season, episode = None):
		'''A private method for requesting either a season or an episode page.

		serie   - serie id as appears on website
		season  - season number
		episode - episode number (omit this arg to request a season)

		Returns either a dictionary or a list of dictionaries holding the content of the loaded webpage 
		'''

		headers = Sdarot._HEADERS

		if episode:
			data_list = ('watch=false', 'serie=%d' % serie, 'season=%d' % season, 'episode=%d' % episode)
		else:
			data_list = ('episodeList=true', 'serie=%d' % serie, 'season=%d' % season)

		data = '&'.join(data_list)
		headers['Content-Length'] = '%d' % len(data)

		req = urllib2.Request(r'http://www.sdarot.tv/ajax/watch', data, headers)
		res = urllib2.urlopen(req)

		return json.loads(res.read())

	@staticmethod
	def _download(url, filename):
		'''A private method for downloading content and saving it to a local
		file.

		url      - a fully qualified path of the remove file to download
		filename - file name for output file (will be created if not exists)
		'''

		res = urllib2.urlopen(url, timeout = 5)

		total_size = int(res.info().getheaders('Content-Length')[0])
		curr_size = 0
		buffer = True

		with open(filename, 'wb') as outfile:
			while buffer:
				buffer = res.read(Sdarot._BUFFER_SIZE)

				if buffer:
					curr_size += len(buffer)

					status = '%3.02f%%' % (curr_size / float(total_size) * 100)
					print '%s%s' % (status, '\x08' * (len(status) + 1)),

					outfile.write(buffer)
			print

	@staticmethod
	def _episode_url(epi):
		if epi.has_key('error'):
			raise LookupError()

		epi['sd'] = epi['watch']['sd']

		return r'http://%(url)s/watch/sd/%(VID)s.mp4?token=%(sd)s&time=%(time)d' % epi

	@staticmethod
	def download_episode(serie, season, episode):
		'''Download a single episode.
		Press Ctrl+C to cancel current download.

		serie   - serie id as appears on website
		season  - season number
		episode - episode number

		See 'get_episodes_list'
		'''

		print 'downloading episode %02d ...' % episode,

		try:
			epi = Sdarot._request_page(serie, season, episode)

			url = Sdarot._episode_url(epi)
			filename = '%s-%02dx%02d.mp4' % (serie, season, episode)

			Sdarot._download(url, filename)
		except LookupError:
			print 'error!'
			time.sleep(1.337)

		except KeyboardInterrupt:
			print 'cancelled by user'

	@staticmethod
	def get_episodes_list(serie, season):
		'''Fetch episodes list of a specified season.

		serie  - serie id as appears on website
		season - season number

		Returns a list of episodes numbers
		'''

		jobj = Sdarot._request_page(serie, season)

		return [int(episode['episode']) for episode in jobj]

	@staticmethod
	def download_season(serie, season):
		'''Download all available episodes for a specified season.
		Press Ctrl+C once to cancel current download, twice to cancel all.

		serie  - serie id as appears on website
		season - season number
		'''

		episodes_list = Sdarot.get_episodes_list(serie, season)
		print '[i] season consists of %d episodes' % len(episodes_list)

		try:
			for episode in episodes_list:
				Sdarot.download_episode(serie, season, episode)
		except KeyboardInterrupt:
			print 'terminated by user'

if __name__ == '__main__':
	from sys import argv

	iargs = map(int, argv[1:])

	if len(iargs) < 2:
		print 'usage: %s serie season [episode]' % argv[0]

	elif len(iargs) == 2:
		Sdarot.download_season(*iargs)

	elif len(iargs) == 3:
		Sdarot.download_episode(*iargs)

# end
