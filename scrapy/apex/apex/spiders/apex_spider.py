"""
Jaracah Teague
Apex - Scrapy
02/21/22

References:
-> https://docs.scrapy.org/en/latest/topics/selectors.html
-> https://coderslegacy.com/python/scrapy-css-selectors-tutorial/
-> https://www.tutorialspoint.com/scrapy/scrapy_selectors.htm
-> https://stackoverflow.com/questions/33140457/scrapy-overwrite-json-files-instead-of-appending-the-file/33487592 

1) Scrapes the top 100 players list for apex legends and returns a dictionary of 12 attributes for each one 
   and includes one fixed item type attribtute to distiguish between player stats and other types of items.

2) Scrapes the legend meta first on the homepage of the website, this is a dictionary of the top four most played legends.
   This includes four attributes plus one fixed item type attribute This is can be dumped in a separate file or yielded

3)Change the overwrite variable below to true to overwrite the previous file (given that the name is data.jl). 
-> I added this functionality to save my self from typing since scrapys overwrite isnt working for me.

"""

import scrapy
import os
import json

# change overwrite to turn on/off
# change separate_meta_legends to false to dump in a separate file
separate_meta_legends = True
overwrite_output = True


if overwrite_output:
	if "data.jl" in os.listdir('.'):
		os.remove('./data.jl')
	if "meta.jl" in os.listdir('.'):
		os.remove('./meta.jl')

class ApexSpider(scrapy.Spider):

	name = 'apex'
	start_url = 'https://apex.tracker.gg/apex/leaderboards/stats/all/RankScore?country=us&page=1'

	def start_requests(self):
		urls = [
			'https://apex.tracker.gg/apex/leaderboards/stats/all/RankScore?country=us&page=1',
			'https://apex.tracker.gg'
		]
		for url in urls:
			# if the url is the base url, callback on the parse_legend_meta function
			if (url == 'https://apex.tracker.gg'):
				yield scrapy.Request(url, callback=self.parse_legends_meta)
				continue
			yield scrapy.Request(url=url, callback=self.parse)
			


	def parse(self, response):
		# get the links of the top 100 user pages and go to them

		for row in response.css('tr'):
			href = row.css('a::attr(href)').get()
			if (not href):
				continue

			#loop through top 100 user pages
			next_page = response.urljoin(href)
			if next_page is not None:
				yield scrapy.Request(next_page, callback=self.parse_player)

	def parse_player(self, response):
		"""
		# parses a player in the top 100 players list
		# yields a dictionary with player attributes

		"""
		# scrape item pages
		# start by getting the title of each page and removing unecessary text
		ret = {'type': 'player_stats'}
		title = response.css('title::text').get().strip(' Stats - Apex Legends Tracker')
		ret['title'] = title
		# filter out bad pages
		if (not title):
				return

		# gets the players userid
		ret['user_id'] = title.strip("'s Apex Legends Overview")

		# gets the players view count
		ret['views'] = response.css('div.ph-details__subtitle > span > span::text').get()
		
		# gets the players stats
		stats = response.css('div.wrapper > div.numbers > span.value::text').getall()
		ret['level'] = stats[0]
		ret['total_kills'] = stats[1]
		ret['total_damage'] = stats[2]
		ret['total_matches'] = stats[3]

		# gets the ranking for the battle royale mode and arenas mode
		rank_label = response.css('div.rating-entry__rank > div > div.rating-entry__rank-info > div.label::text').getall()
		mmr = response.css('div.rating-entry__rank > div > div.rating-entry__rank-info > div.value > span::text').getall()

		ret['br_rank_label'] = rank_label[0].strip()
		ret['br_mmr'] = mmr[0].strip()

		ret['arenas_rank_label'] = rank_label[1].strip()
		ret['areans_mmr'] = mmr[1].strip()

		# gets the last used legends name
		legend = response.css('div.legend__name::text').get()
		ret['recent_legend'] = legend

		# 12 + 1 fixed attribute
		yield ret

	def parse_legends_meta(self, response):
		"""
		# parses the top four most used legends in the current game meta
		# yields a dictionary with the legend meta
		"""
		ret = {'type': 'legend_meta'}
		legends = response.css('div.legend-insights > div.legend-insights__name::text').getall()
		ret['first'] = legends[0]
		ret['second'] = legends[1]
		ret['third'] = legends[2]
		ret['fourth'] = legends[3]
		if (separate_meta_legends):
			with open('meta.jl', 'w') as fp:
				json.dump(ret, fp)
		else:
			yield ret