import os
import pandas as pd
import sys
import numpy as np


def main(input_path, output_path, mode):

    df = pd.read_csv(os.path.join(input_path, "index.txt"),
                     sep="\t", header=0, encoding='latin-1')
    print(f"Currently cached: {len(df)}")

    error_files = []
    combined = []
    for i, entry in enumerate(df.index):
        try:
            print(df.loc[entry].file_name)
            data = pd.read_csv(os.path.join(
                input_path, df.loc[entry].file_name), header=0, encoding='latin-1')
            for i, column in enumerate(data.columns):
                hxl = [None, None]
                if not pd.isna(data.iloc[0][column]):
                    hxl = data.iloc[0][column].split("+")
                if mode == 'flat':
                    for j, row in enumerate(data.index):
                        # skip the hxl tag row
                        if j > 0:
                            combined.append({'Header': column,
                                             'Tag': hxl[0],
                                             'Attributes': hxl[1:],
                                             'Data': data.loc[row][column],
                                             'Relative Column Position': i/len(data.columns),
                                             'Dataset_name': df.loc[entry]['title'],
                                             'Organization': df.loc[entry]['organization']})
                else:
                    combined.append({'Header': column,
                                     'Tag': hxl[0],
                                     'Attributes': hxl[1:],
                                     'Data': list(data.iloc[1:][column]),
                                     'Relative Column Position': i/len(data.columns),
                                     'Dataset_name': df.loc[entry]['title'],
                                     'Organization': df.loc[entry]['organization']})
        except pd.errors.ParserError:
            print(f"Can't open file: {df.loc[entry].file_name}")
            error_files.append({df.loc[entry].file_name})
        except AttributeError:
            print(f"File might not be HXL: {df.loc[entry].file_name}")
            error_files.append({df.loc[entry].file_name})
        if i % 10 == 0:
            out = pd.DataFrame(combined)
            out.to_csv(output_path)

    out = pd.DataFrame(combined)
    out.to_csv(output_path)

    print(f"Completed with {len(error_files)} failures")
    if len(error_files) > 0:
        print("Failed:")
        print(error_files)


if __name__ == "__main__":
    OUTPUT_PATH = None
    INPUT_FILES_DIR = os.path.join("..", os.getcwd(), 'datasets')
    MODE = 'agg'

    args = [x for x in sys.argv[1:] if x.find("=") < 0]
    kwargs = {y[0]: y[1]
              for y in [x.split("=") for x in sys.argv[1:] if x.find("=") > 0]}

    if 'input' in kwargs:
        INPUT_FILES_DIR = kwargs['input']

    if 'mode' in kwargs:
        if kwargs['mode'] not in ['flat', 'agg']:
            raise Exception("Invalid mode option")
        MODE = kwargs['mode']
    if 'output' in kwargs:
        OUTPUT_PATH = kwargs['output']
    else:
        if MODE == 'agg':
            OUTPUT_PATH = os.path.join(
                "..", os.getcwd(), 'aggregated_tag_data.csv')
        else:
            OUTPUT_PATH = os.path.join(
                "..", os.getcwd(), 'flattened_tag_data.csv')

    main(INPUT_FILES_DIR, OUTPUT_PATH, MODE)
