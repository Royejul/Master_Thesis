# The code used in this document was developed specifically for the thesis titled :
# "Comparative Analysis of Statistical and Machine Learning Methods for Topic Modeling of Research Paper Datasets"
# author = Julien Feuillade
# last version from 03 July 2023

import os
import PyPDF2
import json
from tqdm import tqdm
import re

import random

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from nltk.corpus import words

def clean_text(text):
    """
    Cleans and preprocesses the input text.

    Parameters:
        - text (str): The input text to be cleaned.

    Returns:
        - str: The cleaned and preprocessed text.
    """

    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()

    # Tokenize the text
    tokens = nltk.word_tokenize(clean_text)

    # Convert to lowercase
    tokens = [token.lower() for token in tokens]

    # Remove punctuation and special characters
    tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
    tokens = [token for token in tokens if token]

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    tokens = [re.sub(r'\d+', '', token) for token in tokens]
    # Remove tokens with less than 3 characters
    tokens = [token for token in tokens if len(token) >= 3]

    # Convert the words corpus to a set for faster lookups
    english_words = set(words.words())

    # Check if each token exists in the English language
    tokens = [token for token in tokens if token.lower() in english_words]

    # Join the tokens back into a preprocessed string
    preprocessed_text = " ".join(tokens)

    # Encode and decode the text
    return preprocessed_text.encode('cp1252', 'replace').decode('cp1252')

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.

    Parameters:
        - pdf_file (str): The path to the PDF file.

    Returns:
        - Optional[str]: The extracted text from the PDF, or None if an error occurred during processing.
    """

    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            # I don't know why but OCTIS remove always the first word and the last word of the corpus, so i trick the thing
            text += "First "
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            text += "End"
        return text
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Could not process '{pdf_file}'. Skipping...")
        return None

def save_to_json(data, output_file):
    """
    Saves data to a JSON file.

    Parameters:
        - data (Any): The data to be saved to JSON.

        - output_file (str): The path to the output JSON file.

    Returns:
        - None
    """
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def process_pdfs(pdf_folder, output_json):
    """
    Processes PDF files in a specified folder, extracts text from them, and saves the extracted text to a JSON file, with the name of the filename and the text.

    Parameters:
        - pdf_folder (str): The folder containing the PDF files.

        - output_json (str): The path to the output JSON file.

    Returns:
        - None
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    data = []

    for file_name in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        pdf_path = os.path.join(pdf_folder, file_name)
        text = extract_text_from_pdf(pdf_path)
        if text is not None:
            data.append({'File Name': file_name, 'Text': text})

    save_to_json(data, output_json)

def process_pdfs_only_text(pdf_folder, output_json, filename_json):
    """
    Processes PDF files in a specified folder, extracts text from them, and saves the extracted text to JSON files and the name PDF of the text in a other file.
    It's because OCTIS need only the text and not the name but i wanted to keep witch text is associated with witch pdf.
    For exemple : 1st line text of "research_text_10.json" correspond to the 1st line pdf of "research_filename_10.json", etc...

    This function help also to cut the dataset in multiple pourcentage to adapt with OCTIS

    Parameters:
        - pdf_folder (str): The folder containing the PDF files.

        - output_json (str): The path to the output JSON file for storing the extracted text.

        - filename_json (str): The path to the output JSON file for storing the file names.

    Returns:
        - None
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    data = []

    for file_name in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        pdf_path = os.path.join(pdf_folder, file_name)
        text = extract_text_from_pdf(pdf_path)
        if text is not None:
            data.append({'File Name': file_name, 'Text': text})

    # Select a random subset of PDF files for each percentage
    # Depending of the pourcentage of the dataset you want to be split, you should change the value of the line 161 (ex : 1 will take all the dataset)
    for percentage in [0.2, 0.4, 0.6, 0.8, 1]:
        num_files = int(len(pdf_files) * percentage)
        pdf_files_subset = random.sample(pdf_files, num_files)
        data_subset = []
        filename_subset = []

        for file_name in pdf_files_subset:
            for d in data:
                if d['File Name'] == file_name:
                    data_subset.append(d['Text'])
                    filename_subset.append(file_name)
                    break

        output_json_subset = output_json.replace('.json', f'_{int(percentage*100)}.json')
        filename_json_subset = filename_json.replace('.json', f'_{int(percentage*100)}.json')
        save_to_json(data_subset, output_json_subset)
        save_to_json(filename_subset, filename_json_subset)

# Set the input folder containing PDF files and the output JSON file
input_pdf_folder = 'dataset_pdf'
output_json_file = 'dataset_json/research_text.json'
filename_json_file = 'dataset_json/research_filename.json'

# Process the PDF files and save the extracted data to a JSON file
# process_pdfs(input_pdf_folder, output_json_file)
process_pdfs_only_text(input_pdf_folder, output_json_file, filename_json_file)





