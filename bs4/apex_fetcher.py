"""
RobotFetcher.py > apex_fetcher.py
Jaracah Teague
Apex - BS4
02/07/22

Resources Used
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start
https://stackoverflow.com/questions/50613188/how-do-i-create-new-json-data-after-every-script-run

Links to items
https://apex.tracker.gg/
https://apex.tracker.gg/apex/profile/origin/jktheman0467/overview
https://apex.tracker.gg/apex/profile/origin/ernbrz/overview
https://apex.tracker.gg/apex/profile/origin/Skittlecakes/overview
https://apex.tracker.gg/apex/profile/origin/SSG_Dropped/overview
https://apex.tracker.gg/apex/profile/origin/tttcheekyttt_SBI/overview
https://apex.tracker.gg/apex/profile/xbl/nerf%20apex/overview

Attributes
Title - the title of the user page item. Includes username.
Views - Total views of the user profile page item.
Top Four Stats - Retrieves the Player top four stats listed on their user profile page, 
includes kills or level and placement percentage
Legend - retrieves the users last used legend
Rank - retrieves the users current rank in the ranked game mode
Gamemode - Retrieves the last played game mode
Matches - Retrieves the users last played matches and how long ago it was played

Additional Work

scraped all important attributes on the user item page

>5 user pages scraped

if the url is the sites main page, scrape the data about the current legend meta and 
output that in a separate json file, should not execute any further code on that run becuase
it is a separate item page.

"""

from urllib.parse import urlparse
from protego import Protego
from bs4 import BeautifulSoup
import requests
import time
import json
import datetime as dt

class RobotFetcher:

    def __init__(self, user_agent):
        #set user agent and headers
        self.user_agent = user_agent
        self.headers = {'user-agent': user_agent}
        self.crawl_delay = 1
        self.a = []        

    def fetch(self, url):
        """
        Uses user-agent and referrer in requests.get to request a url if it can be fetched 
        (according to the robots.txt). Make sure it waits for crawl delay before fetching again.

        :param url: the url to fetch
        :return: a response object or None (if it can't be fetched.)
        """

        #make sure site can be fetched
        if not self.can_fetch(url):
            print("Can't fetch site. ")
            return None

        # Honor crawl delay
        time.sleep(self.crawl_delay)

        #get site and parse
        r = requests.get(url, headers=self.headers)

        return r

    def scrape(self, url):

        # get response object from fetch and parse
        r = self.fetch(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # create and init item dictionary for this run
        item_dict = {}

        # sets time of script run - for json names, etc
        time_run = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        # page title
        title = soup.select("title")
        item_dict['Title'] = title[0].get_text()


        # ---------------------------------------------------------------------------------
        # if the url is the main page
        if (url == 'https://apex.tracker.gg/'):
            meta = soup.find_all("div", class_="legend-insights")
            inc = 1
            for i in meta:
                self.a.append({"MetaLegend_{}".format(inc): i.get_text()})
                item_dict['MetaLegend__{}'.format(inc)] = i.get_text()
            return
        # 
        # ---------------------------------------------------------------------------------


        #  user name
        # <span class="trn-ign__username">Jktheman0467</span>
        user = soup.find("span", class_="trn-ign__username").get_text()
        item_dict['User'] = user

        # page views
        views = soup.find("span", "title"=="level")
        item_dict['Views']= views.get_text()


        # getting the top four stats for a user
        numbers = soup.find_all("div", class_="numbers")
        inc = 1
        for i in numbers[:4]:
            item_dict['TopFourStats_{}'.format(inc)] = i.get_text()
            inc = inc + 1

    
        # most recent legend
        legend = soup.find("div", class_="legend__name")
        item_dict['RecentLegend'] = legend.get_text()

        # ranking
        rank = soup.find_all("div", class_="text") 
        for i in rank:
            item_dict['Rank'] = i.get_text()

        # recent matches
        matches = soup.find_all("div", class_="match-row")

        # recent mode
        mode = soup.find("div", class_="match-row__label").get_text()
        item_dict['Gamemode'] = mode

        # recent match
        for i in matches:
            item_dict['RecentMatches'] = i.get_text()

        # append item_dict to list for this run
        self.a.append(item_dict)

        


    def can_fetch(self, url):
        """
        Returns whether or not the url can be fetched according to its robots.txt file.

        :param url: url to fetch
        :return: True/False (can be fetched)
        """

        # get robots url
        # request the url and parse
        rp = self.parse_robots(url)


        # crawl delay
        self.crawl_delay = rp.crawl_delay(self.user_agent)
        if not self.crawl_delay:
            self.crawl_delay = 1

        # can fetch
        return rp.can_fetch(url, self.user_agent)

    def get_robots_url(self, url):
        o = urlparse(url)
        robots_url = o.scheme + '://' + o.hostname + '/robots.txt'
        return robots_url    

    def parse_robots(self, url):
        robots_url = self.get_robots_url(url)
        r = requests.get(robots_url, headers=self.headers)
        rp = Protego.parse(r.text)
        return rp

def main():
    rf = RobotFetcher("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")
    
    # url = "https://apexlegendsstatus.com/profile/PC/jktheman0467"
    url1 =  "https://apex.tracker.gg/apex/profile/origin/jktheman0467/overview"
    url2 = "https://apex.tracker.gg/apex/profile/origin/ernbrz/overview"
    url3 = "https://apex.tracker.gg/apex/profile/origin/Skittlecakes/overview"
    url4 = "https://apex.tracker.gg/apex/profile/origin/SSG_Dropped/overview"
    url5 = "https://apex.tracker.gg/apex/profile/origin/tttcheekyttt_SBI/overview"

    url = "https://apex.tracker.gg/"

    rf.scrape(url1)
    rf.scrape(url2)
    rf.scrape(url3)
    rf.scrape(url4)
    rf.scrape(url5)
    rf.scrape(url)

    with open('apex.json', 'w') as fp:
            json.dump(rf.a, fp)

if __name__ == "__main__":
    main()
#    url = (input("Input a URL: "))
#    print (url)

