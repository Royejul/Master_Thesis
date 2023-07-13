# Comparative Analysis of Statistical and Machine Learning Methods for Topic Modeling of Research Paper Datasets
Here is the code for the Master's thesis.

## Installation
First, make sure to have the ```dataset_octis``` folder, otherwise it will be impossible to try out the various models.

The project requires Python 3.10 (or a later version). It is recommended to use a virtual environment to install the necessary dependencies.

You can set up a virtual environment and install the dependencies as follows:

```bash
# Clone the repository
git clone https://github.com/Royejul/Master_Thesis.git
cd Master_Thesis

# Set up virtual environment (Windows)
python -m venv env
env\Scripts\activate

# Set up virtual environment (Unix/MacOS)
python3 -m venv env
source env/bin/activate

# Install the requirements
pip install -r requirements.txt

# Start Jupyter
jupyter notebook
```

A new web page will open (with your Jupyter localhost) then open the file ```model_evaluation.ipynb```. This is the main file where the different models are launched and then run the various proposed blocks. The first block only concerns data extraction, only run it if you want new data for our models.

The ```model.py``` file stores the code for the models, coherence, diversity and computation time. It is then used by the Jupyter file ```model_evaluation.ipynb```.

The ```extract_pdf_from_arxiv.py``` file is only useful for extracting PDFs from the ```export.arxiv.org``` website.

The ```pdf_to_json.py``` file is used to extract the text from the PDFs in the ```dataset_pdf``` folder, so make sure to have the same folder name or modify the name directly in the code. Then run the file and it automatically extracts the files.
