"""
# Jaracah Teague
# CS3435 - Program 4 Selenium
# Appalachian State University
"""

# imports
import selenium
from selenium import webdriver
import json
import time
import os

# options
overwrite = True
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
# getting leaderboard data

# go to the leaderboard page
driver.get(leaderboard)
time.sleep(2)

# get all hrefs in table and loop

links = driver.find_elements_by_css_selector('tr > td.username > div.text > a')
link_hrefs = [link.get_attribute('href') for link in links]


for link in link_hrefs:
	driver.get(link)
	time.sleep(2) # wait
	# create data and append to json lines file
	driver.back()
	time.sleep(2)
	data = {
	
		'name': 'name',

	}

	with open('apex.jl', 'a') as fp:
		fp.write(json.dumps(data))

#
# -----------------------------------------------------------------------------------------------------



# close webdriver
driver.close()
