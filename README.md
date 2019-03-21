# hdx-python-model
Jupyter Notebook of the Model


The Python file contains the ML model used by the API. The output of the model generates a pickle file (for the API) and top 3 predicted tags for a given header with their respective confidence levels.   

To run the python notebook, follow the instructions below:

1) [Install HDX Python Library](https://github.com/OCHA-DAP/hdx-python-api)
2) [Install nltk](https://www.nltk.org/install.html)
3) Install fastText: <br />
    a) git clone https://github.com/facebookresearch/fastText.git <br />
    b) cd fastText <br />
    c) pip install . <br />
    d) [download word vectors](https://fasttext.cc/docs/en/pretrained-vectors.html). Make sure to download 'English: bin+text' to the same folder as the model.<br />
4) Create a folder called 'datasets' in the same directory the python notebook is stored in. This is where datasets scraped from HDX will be stored temporarily.
5) [Install Scikit](https://scikit-learn.org/stable/install.html)
6) Make sure that your directory includes the training dataset 'headertag_fulldataset.xlsx', which includes the pruned data of all the tagged datasets in HDX as of 3/15/2019. 
7) Make sure to have the correct parameters for the model given in the first cell of the python file: <br />
    a)create_dataset (default: False) - boolean to determine whether the user want to download from HDX database vs. pre-loaded excel file <br />
    b)SAMPLE_NUMBER_OF_DATASETS (default: 150) - number of training datasets to scrape from HDX database 
