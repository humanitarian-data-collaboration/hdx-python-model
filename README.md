# hdx-python-model
Jupyter Notebook of the Model


The Python file contains the ML model used by the API. The output of the model generates a pickle file (for the API) and top 3 predicted tags for a given header with their respective confidence levels.   

To run the python notebook, follow the instructions below:


0) Optional: Create a virtual environment and install an ipython kernel
	+ Plain python:
		+ `python -m venv .venv`
		+ `.venv\Scripts\activate[.ps1 or other appropriate suffix]`
		+ `python -m ipykernel install --user --name hdx-model`
	+ Conda:
		+ `conda create -n hdx-model`
		+ `source activate hdx-model`
		+ `python -m ipykernel install --name hdx-model`
1) Install requirements
	+ fasttext requires a C++ compiler. On Windows platforms this will require an additional installation. Mac and Linux platforms should have a compiler pre-installed.
	+ `pip install -r requirements.txt`
2) Make sure that your directory includes the training dataset 'headertag_fulldataset.xlsx', which includes the pruned data of all the tagged datasets in HDX as of 3/15/2019. 
3) Open the notebook in jupyter.  Select the `hdx-model` kernel that we created earlier.
4) Make sure to have the correct parameters for the model given in the first cell of the python file:
    + create_dataset (default: False) - boolean to determine whether the user want to download from HDX database vs. pre-loaded excel file
    + SAMPLE_NUMBER_OF_DATASETS (default: 150) - number of training datasets to scrape from HDX database 
5) Run the notebook. It will take at least one major setup action:
	+ Downloading the pre-trained word vectors if they do not exist. This is an ~8GB download.