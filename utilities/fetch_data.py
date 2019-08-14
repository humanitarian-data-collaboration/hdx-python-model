from hdx.utilities.easy_logging import setup_logging
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.utilities.downloader import DownloadError
import os
import pandas as pd
import sys
from datetime import datetime


def main(limit, output):

    # datasets scraped from HDX will be stored here
    try:
        os.makedirs(RAW_DATA_DIR)
    except:
        pass

    # Setting up account connection to HDX Database
    setup_logging()
    Configuration.create(
        hdx_site='prod', user_agent='A_Quick_Example', hdx_read_only=True)

    # set up indexing so that we don't re-fetch the same file twice
    index_path = os.path.join(RAW_DATA_DIR, 'index.txt')
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            f.write(
                f"dataset_id\trevision_last_updated\tresource_id\tfile_name\ttitle\torganization\n")
    index = pd.read_csv(index_path, sep="\t", header=0,
                        index_col=0, encoding='latin-1')
    print(f"Currently cached: {len(index)}")
    # the search_in_hdx query supports SOLR, but I can't find a way to filter on children
    # if possible we'd want to filter for tags:[name: hxl] and resources:[type: CSV]

    hxl_datasets = Dataset.search_in_hdx('hxl', rows=limit)
    print(f"Found {len(hxl_datasets)} possible datasets with HXL")

    download_failures = []
    for i, dataset in enumerate(hxl_datasets):
        if 'hxl' in dataset.get_tags() and 'CSV' in dataset.get_filetypes():
            res = dataset.resources[dataset.get_filetypes().index('CSV')]
            try:
                existing_row = index.loc[dataset['id']]
                # switch to the specific resource in the cache
                # sometimes there are multiple CSV resources
                # if HXLated is in the name, it's probably that one
                res = Resource.read_from_hdx(existing_row['resource_id'])
                if res['revision_last_updated'] == existing_row['revision_last_updated']:
                    continue
            except KeyError:
                pass

            try:
                url, path = res.download(RAW_DATA_DIR)
                # taking a performance hit here by writing for every file
                # but it makes the download more robust
                with open(index_path, 'a') as f:
                    f.write(
                        f"{dataset['id']}\t{res['revision_last_updated']}\t{res['id']}\t{os.path.basename(path)}\t{dataset['title']}\t{dataset['organization']['title']}\n")
                print(f"Downloaded #{i}: {path}")
            except DownloadError:
                print(f"Failed to download: {dataset['title']}")
                download_failures.append((dataset['title'], dataset['id']))
    print(f"Completed with {len(download_failures)} failures")
    if len(download_failures) > 0:
        print("Failed:")
        print(download_failures)


if __name__ == "__main__":
    LIMIT = 1000
    RAW_DATA_DIR = os.path.join("..", os.getcwd(), 'datasets')

    args = [x for x in sys.argv[1:] if x.find("=") < 0]
    kwargs = {y[0]: y[1]
              for y in [x.split("=") for x in sys.argv[1:] if x.find("=") > 0]}

    if 'limit' in kwargs:
        try:
            LIMIT = int(kwargs['limit'])
        except:
            raise Exception("Limit argument must be an integer")
    if 'output' in kwargs:
        RAW_DATA_DIR = kwargs['output']

    main(LIMIT, RAW_DATA_DIR)
