from bs4 import BeautifulSoup
import logging
import requests
import yagmail
import time
import os

password = os.getenv("passwd")

message = """\
There was an update on Manitoba's covid 19 website. Check it out at:

https://www.gov.mb.ca/covid19/updates/index.html
"""

datestr = "Last updated: April 4, 2021"

url = "https://www.gov.mb.ca/covid19/updates/index.html"

def check():
    log = logging.getLogger(__name__)
    while True:
        raw = requests.get(url)
        soup = BeautifulSoup(raw.content, 'html.parser')
        dateraw = soup.find_all("em")
        date = dateraw[0].get_text()
        global datestr
        global password
        global message
        if datestr != date:
            yag = yagmail.SMTP(user="covidalerter7@gmail.com", password=password)
            yag.send(to="runkedillon@gmail.com", subject="New COVID info from Manitoba", contents=message)
            datestr = date
            log.warning(f"Datestr updated to {date}")
            time.sleep(500)
            check()
        else:
            time.sleep(500)
            check()

check() 