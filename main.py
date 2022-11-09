# you may need to install apt-get install python3-lxml
# inspired by Tom's Scotts project

import requests
from bs4 import BeautifulSoup
import os.path
from mastodon import Mastodon
import time

mastodon = Mastodon(
    access_token = 'YOURTOKEN',
    api_base_url = 'https://social.linux.pizza'
)
#mastodon.toot('Tooting from python using #mastodonpy !')

#############################################
#
# IMPORTANT DETAILS
ip_range = "153.31.0.0"
block = "16"
#
#############################################


url = "https://en.wikipedia.org/w/api.php?action=feedcontributions&user=" + ip_range + "%2F" + block + "&feedformat=rss"
a = requests.get(url, headers={"User-agent": "Fedits"})
s = BeautifulSoup(a.text, "lxml-xml")


if os.path.exists("lastedit") == False:
    for g in s.find_all("item", limit=1):
        print("This is your first time running the program!")
        print("The newest edit from the FBI is: " + g.pubDate.text)
        mastodon.toot("Hello, world! Here is the lastest edit from the FBI: " + g.link.text)
        print("Writing to the disk...")
        with open('lastedit', 'a') as f:
            f.write(g.pubDate.text)

while True:
    print("30 second cooldown")
    time.sleep(30)
    url = "https://en.wikipedia.org/w/api.php?action=feedcontributions&user=" + ip_range + "%2F" + block + "&feedformat=rss"
    a = requests.get(url, headers={"User-agent": "Fedits"})
    s = BeautifulSoup(a.text, "lxml-xml")
    for g in s.find_all("item", limit=1):
        with open('lastedit', 'r') as p:
            txt = p.read()
        if g.pubDate.text != txt:
            print("NEW EDIT: " + g.link.text + " @ " + g.pubDate.text)
            mastodon.toot("New edit: " + g.link.text + " , timestamp: " + g.pubDate.text)
        else:
            print("No new edits since " + txt)
