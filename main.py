from bs4 import BeautifulSoup
import logging
import requests
import yagmail
import time
import os
import pymongo

client = pymongo.MongoClient(
    os.getenv("MKEY")
)

password = os.getenv("passwd")

datestr = "Last updated: April 4, 2021"

message = f"""\
There was an update made on Manitoba's covid 19 website. Check it out at:

https://www.gov.mb.ca/covid19/updates/index.html

{datestr}
"""

url = "https://www.gov.mb.ca/covid19/updates/index.html"

def check():
    log = logging.getLogger(__name__)
    while True:
        global client
        db = client.COVID_TRACKER
        collection = db.Emails
        rawusers = collection.find_one({}, {"_id": 0})
        log.warning("Obtained emails.")
        emails = rawusers.get("emails")
        raw = requests.get(url)
        soup = BeautifulSoup(raw.content, 'html.parser')
        dateraw = soup.find_all("em")
        date = dateraw[0].get_text()
        global datestr
        global password
        global message
        if datestr != date:
            datestr = date
            log.warning(f"Datestr updated to {date}")
            yag = yagmail.SMTP(user="covidalerter7@gmail.com", password=password)
            for email in emails:
                yag.send(to=email, subject="New COVID info from Manitoba", contents=message)
            time.sleep(500)
            check()
        else:
            time.sleep(500)
            check()

check() 