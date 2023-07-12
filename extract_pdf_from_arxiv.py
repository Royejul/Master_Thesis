# The code used in this document was developed specifically for the thesis titled :
# "Comparative Analysis of Statistical and Machine Learning Methods for Topic Modeling of Research Paper Datasets"
# author = Julien Feuillade
# last version from 03 July 2023

import os
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Define the base URL for the Computer Science category on arXiv.org
base_url = "https://export.arxiv.org/list/"

# Define a list of subcategories in Computer Science
categories = ["cs.AI", "cs.CL", "cs.CC", "cs.CE", "cs.CG", "cs.GT", "cs.CV", "cs.CY", "cs.CR", "cs.DS", "cs.DB",
              "cs.DL", "cs.DM", "cs.DC", "cs.ET", "cs.FL", "cs.GR", "cs.AR", "cs.HC", "cs.IR", "cs.IT", "cs.LG",
              "cs.LO", "cs.MS", "cs.MA", "cs.MM", "cs.NI", "cs.NE", "cs.NA", "cs.OH", "cs.PF", "cs.PL", "cs.RO",
              "cs.SI", "cs.SE", "cs.SD", "cs.SC", "cs.SY"]

# Define the number of PDF files to download for each category
num_pdfs_per_category = 10

# Specify the path of the folder where you want to save the PDF files
folder_path = "dataset_pdf"

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Loop through each subcategory
for i in range(1):
    for category in categories:
        # Initialize a flag to keep track of whether the PDF files were successfully downloaded
        downloaded = False

        # Initialize a list to keep track of the PDF files that have already been downloaded
        downloaded_files = []

        while not downloaded:
            # Get the current date and time
            now = datetime.now()
            # Generate a random year between 2020 and the current year
            year = random.randint(2016, 2022)
            month = random.randint(1, 12)
            # Construct a date string in the format "YYMM" (e.g., "2212" for December 2022)
            date_str = "{:02d}{:02d}".format(year % 100, month)
            # Construct the URL for the page listing papers in the subcategory for the random month and year
            url = base_url + category + "/" + date_str
            print(url)

            try:
                # Make a request to the URL and parse the HTML content
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                # Find all the links to PDF files on the webpage
                pdf_links = soup.find_all("a", title="Download PDF")
                print(pdf_links)
                # Exclude the PDF files that have already been downloaded
                pdf_links_to_download = [link for link in pdf_links if os.path.join(folder_path,
                                                                                    link['href'].split('/')[
                                                                                        -1]) + "_" + category + '.pdf' not in downloaded_files]
                # Choose 10 links at random
                pdf_links_to_download = random.sample(pdf_links_to_download,
                                                      min(num_pdfs_per_category, len(pdf_links_to_download)))
                # Download each PDF file and save it in the folder
                for link in pdf_links_to_download:
                    pdf_url = 'https://export.arxiv.org' + link['href']
                    filename = os.path.join(folder_path, pdf_url.split('/')[-1]) + "_" + category + '.pdf'
                    if os.path.exists(filename):
                        print(f"File {filename} already exists. Skipping download.")
                    else:
                        with open(filename, 'wb') as f:
                            response = requests.get(pdf_url)
                            f.write(response.content)
                        # Add the downloaded file to the list of downloaded files
                        downloaded_files.append(filename)
                # Set the flag to indicate that the PDF files were successfully downloaded
                downloaded = True
            except:
                print(f"An error occurred while trying to access the URL {url}. Trying again with a new date.")
                # Generate a new set of random year and month values and try again
                continue
