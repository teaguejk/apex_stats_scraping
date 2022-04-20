"""
# Jaracah Teague
# Apex - Final Project
# Appalachian State University
# 04/20/22
"""

# -----------------------------------------------------------------------------------------------------
# Set Up

# imports
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
import os

# options
overwrite = False
headless = False

# urls
home = 'https://apex.tracker.gg/'
leaderboard = 'https://apex.tracker.gg/apex/leaderboards/stats/all/RankScore?page=1'

# overwirte output file
if overwrite:
	if "apex.jl" in os.listdir('.'):
		os.remove('./apex.jl')

# create webdriver
if headless:
	# headless mode
	options = webdriver.FirefoxOptions()
	options.headless = True
	driver = webdriver.Firefox(options=options)
else:
	driver = webdriver.Firefox()

# -----------------------------------------------------------------------------------------------------
# get leaderboard data
try:
	# go to the leaderboard page
	driver.get(home)
	# driver.get(leaderboard)
	time.sleep(1)

# ==================================================================================================
	# get my page first
	textbox = driver.find_element_by_css_selector('.search-box__bar > form:nth-child(2) > input:nth-child(1)')
	time.sleep(1)
	textbox.click()
	time.sleep(1)
	textbox.send_keys('jktheman0467')
	textbox.send_keys(Keys.ENTER)
	time.sleep(1)

	# getting data values from the page

	# player id
	user_id = driver.find_element_by_css_selector('span.trn-ign__username').text

	# views 
	views = driver.find_element_by_css_selector('div.ph-details__subtitle > span > span').text

	# stats --neds to be fixed
	stats 	= driver.find_elements_by_css_selector('div.wrapper > div.numbers > span.value')
	level 	= stats[0].text
	kills 	= stats[1].text
	# damage 	= stats[2].text
	# matches = stats[3].text

	# ranked and arenas stats
	rank 	= driver.find_elements_by_css_selector('div.rating-entry__rank > div > div.rating-entry__rank-info > div.label')
	mmr 	= driver.find_elements_by_css_selector('div.rating-entry__rank > div > div.rating-entry__rank-info > div.value > span')

	br_rank = rank[0].text.strip()
	br_mmr 	=  mmr[0].text.strip()

	ar_rank = rank[1].text.strip()
	ar_mmr 	=  mmr[1].text.strip()

	# gets most recently used legend
	legend = driver.find_element_by_css_selector('div.legend__name').text

	# create data and append to json lines file
	data = {
	
		'user_id'	: user_id,
		'views'		: views,
		'level'		: level,
		'kills'		: kills,
		# 'damage'	: damage,
		# 'matches'	: matches,
		'br_rank'	: br_rank,
		'br_mmr'	: br_mmr,
		'ar_rank'	: ar_rank,
		'ar_mmr'	: ar_mmr,
		'legend'	: legend,

	}

	with open('apex.jl', 'a') as fp:
		fp.write(json.dumps(data))
		fp.write('\n')

# ==================================================================================================
# begin getting leaderboard data

	driver.find_element_by_css_selector('li.item:nth-child(3) > a:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)').click()
	time.sleep(1)

	# get all hrefs in table and loop
	links = driver.find_elements_by_css_selector('tr > td.username > div.text > a')
	link_hrefs = [link.get_attribute('href') for link in links]

	# looping through each page
	for link in link_hrefs:

		# filter bad links
		if "twitch" in link:
			continue
		elif "twitter" in link:
			continue

		# go to link and wait --possibly use wait for element functions
		driver.get(link)
		time.sleep(1) 

		# ==================================================================================================
		# getting data values from the page

		# player id
		user_id = driver.find_element_by_css_selector('span.trn-ign__username').text

		# views 
		views = driver.find_element_by_css_selector('div.ph-details__subtitle > span > span').text

		# stats --neds to be fixed
		stats 	= driver.find_elements_by_css_selector('div.wrapper > div.numbers > span.value')
		level 	= stats[0].text
		kills 	= stats[1].text
		# damage 	= stats[2].text
		# matches = stats[3].text

		# ranked and arenas stats
		rank 	= driver.find_elements_by_css_selector('div.rating-entry__rank > div > div.rating-entry__rank-info > div.label')
		mmr 	= driver.find_elements_by_css_selector('div.rating-entry__rank > div > div.rating-entry__rank-info > div.value > span')

		br_rank = rank[0].text.strip()
		br_mmr 	=  mmr[0].text.strip()

		ar_rank = rank[1].text.strip()
		ar_mmr 	=  mmr[1].text.strip()

		# gets most recently used legend
		legend = driver.find_element_by_css_selector('div.legend__name').text

		# ==================================================================================================


		# create data and append to json lines file
		data = {
		
			'user_id'	: user_id,
			'views'		: views,
			'level'		: level,
			'kills'		: kills,
			# 'damage'	: damage,
			# 'matches'	: matches,
			'br_rank'	: br_rank,
			'br_mmr'	: br_mmr,
			'ar_rank'	: ar_rank,
			'ar_mmr'	: ar_mmr,
			'legend'	: legend,

		}

		with open('apex.jl', 'a') as fp:
			fp.write(json.dumps(data))
			fp.write('\n')

# -----------------------------------------------------------------------------------------------------
# close webdriver
except:
	driver.quit()

finally:
	driver.quit()
