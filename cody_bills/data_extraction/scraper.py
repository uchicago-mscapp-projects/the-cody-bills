import json
import os
import requests
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path

with open("key.txt", "r") as f:
    key = f.read()

STATES = ["Pennsylvania", "Texas"]
DATE_CREATED = "2022-01-01"

for state in STATES:

    # We create this page file in case the requests per day are limited
    # so that we can continue the next day with the same key in the page
    # where we finish the previous day
    # page_path = Path(f"page_{state}.txt")
    # if not page_path.is_file():
    #     with open(f"page_{state}.txt", "w") as f:
    #         file.write('1')

    with open(f"page_{state}.txt", "r") as f:
        page = int(f.read())

    bills_dictionary = dict()
    for i  in range(3):#while True:
        url = f"https://v3.openstates.org/bills?jurisdiction={state}&created_since={DATE_CREATED}&sort=updated_desc&include=versions&page={page}&per_page=20&apikey=" + key
        request1 = requests.get(url)
        bills_lst = json.loads(request1.text)["results"]
        n_bills = 0
        for bill in bills_lst:
            if not bill["versions"]: #only getting bills that have links
                continue
            bill_dict = dict()
            bill_dict["id"] = bill["id"]
            bill_dict["state"] = bill["jurisdiction"]["name"]
            bill_dict["title"] = bill["title"]
            bill_dict["chamber"] = bill["from_organization"]["name"]
            bill_dict["created_date"] = bill["created_at"][:10] # just year, month, day
            for version in bill["versions"]:
                for link in version["links"]:
                    if link["media_type"] == "text/html":
                        bill_dict["link"] = link["url"]
                        html = urlopen(link["url"]).read()
                        soup = BeautifulSoup(html, features="html.parser")
                        for script in soup(["script", "style"]): # cleaning format
                            script.extract()
                        bill_dict["text"] = soup.get_text()
            bills_dictionary[bill["id"]] = bill_dict
            n_bills += 1
        page += 1
        time.sleep(7) # only 10 requests allowed per minute
        if n_bills < 20:
            break

    # append to the end of the file
    with open(f"bills_{state}.json", "a") as f:
        json.dump(bills_dictionary, f, indent = 4)

    with open(f"page_{state}.txt", "w") as f:
        f.write(str(page))
