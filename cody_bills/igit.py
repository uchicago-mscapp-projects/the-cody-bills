

import pandas as pd
import numpy as np

random_california = np.random.randint(low=2, high=10, size=(1000,3))

random_texas = np.random.randint(low=2, high=10, size=(1000,3))

cols = ["Bill", "Description", "Energy Policy Index"]
df_california = pd.DataFrame(random_california, columns = cols)
df_texas = pd.DataFrame(random_texas, columns = cols)

df_california.to_csv("table_california.txt", index = False)
df_texas.to_csv("table_texas.txt", index = False)

###############
import requests

# url = "https://leginfo.legislature.ca.gov/faces/billPdf.xhtml?bill_id=202320240AB1634&version=20230AB163499INT"
url = "https://mgaleg.maryland.gov/2023RS/bills/hb/hb0173f.pdf"
# out = "C:/Users/Pablo/Documents/Classes/Quarter_2/Computer_Science_2/30122-project-the-cody-bills/example_pdf.PDF"
out = "C:/Users/Pablo/Documents/Classes/Quarter_2/Computer_Science_2/Example/example_marlyland.pdf"

r = requests.get(url)

content = r.content
content


with open(out, "r") as file:
    text = file.write(content)

import urllib.request
# url = "https://leginfo.legislature.ca.gov/faces/billPdf.xhtml?bill_id=202320240AB1634&version=20230AB163499INT"
# url = "https://mgaleg.maryland.gov/2023RS/bills/hb/hb0173f.pdf"
url = "https://ilga.gov/legislation/103/SR/PDF/10300SR0083.pdf"
out = "C:/Users/Pablo/Documents/Classes/Quarter_2/Computer_Science_2/Example/example_illinois.pdf"

urllib.request.urlretrieve(url, out)


#########
import requests 
import os

json = {"ocd-bill/5f4fc2bb-4667-4b76-b3f6-64b813d1f57d": "https://leginfo.legislature.ca.gov/faces/billPdf.xhtml?bill_id=202320240AB1634&version=20230AB163499INT",
    "ocd-bill/72396082-dba9-4690-9b8a-0842b78f9cec": "https://leginfo.legislature.ca.gov/faces/billPdf.xhtml?bill_id=202320240AB1524&version=20230AB152499INT",
    "ocd-bill/ee3bcf5a-8afc-4ddd-929a-4350c27fefec": "https://leginfo.legislature.ca.gov/faces/billPdf.xhtml?bill_id=202320240AB1368&version=20230AB136899INT",
    "ocd-bill/bea74a03-3778-46bf-8401-2a5909fc0f19": "https://leginfo.legislature.ca.gov/faces/billPdf.xhtml?bill_id=202320240AB659&version=20230AB65998AMD"}

path = "C:/Users/Pablo/Documents/Classes/Quarter_2/Computer_Science_2/Example/"
for bill, link in json.items():
    response = requests.get(link)
    bill = bill.replace("ocd-bill/","")
    filename = os.path.join(path, f"{bill}.pdf")
    with open(filename, "wb") as f:
        f.write(response.content)

####
import PyPDF2
doc = PyPDF2.PdfReader("example_2.pdf")
text = ""
for page in doc.pages:
    text += page.extract_text()


    # dic_strings["bill"] = text



###########
import pandas as pd

datatable_california = pd.read_csv("cody_bills/assets/table_california.txt").to_dict("records")
datatable_texas = pd.read_csv("cody_bills/assets/table_texas.txt").to_dict("records")




