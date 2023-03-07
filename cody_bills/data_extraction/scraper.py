import json
import os
import requests
import time
from bs4 import BeautifulSoup
from pathlib import Path
from PyPDF2 import PdfReader
from io import BytesIO

# to run this file, one has to open an account in Open States and use 
# their key which comes in the profile

def get_page_number(state):
    '''
    Gets the current page number for a given state from a file.

    Inputs:
        state (str): the state for which to get the current page number

    Returns:
        page (int): the current page number for the given state
    '''
    page_path = Path(f"cody_bills/data_extraction/page_{state}.txt")
    if not page_path.is_file():
        with open(f"cody_bills/data_extraction/page_{state}.txt", "w") as f:
            f.write('1')

    with open(f"cody_bills/data_extraction/page_{state}.txt", "r") as f:
        page = int(f.read())
    
    return page

def read_key(key_file_path):
    '''
    Reads the OpenStates API key from a file and returns it as a string.

    Inputs:
        key_file_path (str): The path to the file containing the API key.

    Returns:
        key (str): The API key as a string.
    '''
    with open(key_file_path, "r") as f:
        key = f.read()
    return key

def get_url(state, date, page_num, key):
    '''
    Constructs and returns a URL for querying bills from the Open States API.

    Inputs:
        state (str): The state jurisdiction for the bills to be queried.
        date (str): The date from which bills were created in the format "YYYY-MM-DD".
        page_num (int): The page number of the bills to be queried.
        key (str): The API key required for accessing the Open States API.

    Returns:
        url (str): The URL for querying bills from the Open States API with 
         the specifications.
    '''
    url = (f"https://v3.openstates.org/bills?jurisdiction={state}&created_since={date}"
               f"&sort=updated_desc&include=versions&page={page_num}"
               f"&per_page=20&apikey=" + key)

    return url

def get_bill_dict(bill):
    '''
    Extracts information from a bill object and returns a dictionary containing 
     relevant data.
    
    Inputs:
        bill (dict): A dictionary containing information about a legislative bill.

    Returns:
        bill_dict (dict): A dictionary containing the information about the bill 
         including the text.
    '''

    if not bill["versions"]: # only getting bills that have links
        return False
    bill_dict = dict()
    bill_dict["id"] = bill["id"]
    bill_dict["state"] = bill["jurisdiction"]["name"]
    bill_dict["title"] = bill["title"]
    bill_dict["chamber"] = bill["from_organization"]["name"]
    bill_dict["created_date"] = bill["created_at"][:10] # just year, month, day
    try: # this is used for the case where a specific pdf or text/html scrape does not work
        text, url = get_bill_text(bill)
        bill_dict["link"] = url
        bill_dict["text"] = text
    except:
        return False

    return bill_dict

def get_bill_text(bill):
    '''
    Returns the plain text of a legislative bill, which is obtained from either 
     an HTML or PDF link.
    
    Inputs:
        bill (dict): A bill object containing information about a legislative bill.

    Returns:
        text (str): The plain text of the bill.
    '''
    if is_html_available(bill):
        text, url = get_html_text(bill)
    else:
        text, url = get_pdf_text(bill)
    
    return text, url

def is_html_available(bill):
    '''
    Determines if an HTML link is available for a legislative bill.

    Inputs:
        bill (dict): A bill object containing information about a legislative bill.

    Returns:
        boolean: True if an HTML link is available for the bill, False otherwise.
    '''
    for version in bill["versions"]:
        for link in version["links"]:
            if link["media_type"] == "text/html":
                return True
            else:
                continue

    return False

def get_html_text(bill):
    '''
    Returns the plain text of a legislative bill obtained from an HTML link.

    Inputs:
        bill (dict): A bill object containing information about a legislative bill.
    
    Returns:
        text (str): The plain text of the bill from the HTML link.
    '''
    bill_dict = dict()
    for version in bill["versions"]:
        for link in version["links"]:
            if link["media_type"] == "text/html":
                html = requests.get(link["url"])
                soup = BeautifulSoup(html.content, features="html.parser")
                for script in soup(["script", "style"]): # cleaning format
                    script.extract()
                text = soup.get_text()
    
    return text, link["url"]

def get_pdf_text(bill):
    '''
    Returns the plain text of a legislative bill obtained from a PDF link.

    Inputs:
        bill (dict): A bill object containing information about a legislative bill.
    
    Returns:
        text (str): The plain text of the bill from the PDF link.
    '''
    for version in bill["versions"]:
        for link in version["links"]:
            if link["media_type"] == "application/pdf":
                response = requests.get(link["url"])
                tempio = BytesIO(response.content)
                doc = PdfReader(tempio)
                text = ""
                for sheet in doc.pages:
                    text += sheet.extract_text()

    return text, link["url"]

def write_bills_and_page_to_file(state, bills, page_num):
    '''
    Appends bills dictionary to file with name "bills_{state}.json"

    Inputs:
        bills (dict): dictionary containing the bills data to write to file
        state (str): state for which the bills data is being written

    Returns:
        None
    '''

    with open(f"cody_bills/data_extraction/bills_{state}.json", "a") as f: #appends to the end of the file
            json.dump(bills, f, indent = 4)

    with open(f"cody_bills/data_extraction/page_{state}.txt", "w") as f:
        f.write(str(page_num))

def scraper(states, date, key):
    '''
    Scrapes data of bills from the Open States API for given list of states and a
    date of creation of the bill and writes the data to a file in json format. It
    also saves the page number for each state to a file in case the requests per
    day are limited. This ensures that the scraping can continue from where it left
    off the next day with the same key in the page where it finished the previous day.

    Parameters:
        states (list): a list of states to scrape bills data for
        date (str): the created date to get the bills since (in yyyy-mm-dd format)
        key (str): the API key to use for making requests to openstates API

    Returns:
        None
    '''
    for state in STATES:
        # Creating a page file and number in case the requests per day are 
        # limited so that we can continue the next day with the same key in 
        # the page where we finish the previous day
        page = get_page_number(state)

        bills_dictionary = dict()
        while True:
            url = get_url(state, DATE_CREATED, page, KEY)
            request1 = requests.get(url)
            bills_lst = json.loads(request1.text)["results"]
            
            n_bills = 0
            for bill in bills_lst:
                bill_dict = get_bill_dict(bill)
                if not bill_dict:
                    continue
                bills_dictionary[bill["id"]] = bill_dict
                n_bills += 1
            
            page += 1
            time.sleep(7) # only 10 requests allowed per minute
            if n_bills < 20: # got to the last page
                break

        write_bills_and_page_to_file(state, bills_dictionary, page)

if __name__ == "__main__":
    KEY = read_key("cody_bills/data_extraction/key.txt") # getting key from local directory
    STATES = ["Texas", "Pennsylvania", "Illinois"] # one state for html and one for pdf
    DATE_CREATED = "2022-01-01" # for bills created 2022-latest data
    scraper(STATES, DATE_CREATED, KEY)
