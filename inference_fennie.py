import os
from sybil import Serie, Sybil
import time
import json
import pandas as pd
import numpy as np
import csv
import traceback

ParentDirectory = "/mnt/netcache/bodyct/experiments/Sybil_Fennie/DLCST/DICOM_files/errorfile2"

#Name of the output csv file
csvoutput = "/mnt/netcache/bodyct/experiments/Sybil_Fennie/DLCST/errorfileresults.csv"

log_file = "/mnt/netcache/bodyct/experiments/Sybil_Fennie/DLCST/script_log7.txt"

start_time_model = time.time()
# Load a trained model
model = Sybil("sybil_base")

def get_subfolder_paths(parent_folder):
    """Return a list of all subfolder paths in a parent folder.

    Parameters:
    parent_folder (str): The path to the parent folder.

    Returns:
    List[str]: A list of paths for all subfolders in the parent folder.
    """
    subfolder_names = os.listdir(parent_folder)
    subfolder_paths = [os.path.join(parent_folder, name) for name in subfolder_names if os.path.isdir(os.path.join(parent_folder, name))]
    return subfolder_paths

def get_dcm_filepaths(folder_path):
    """Parse through a folder of .dcm files and return a list of all file paths.

    Parameters:
    folder_path (str): The path to the folder containing the .dcm files.

    Returns:
    List[str]: A list of file paths for all .dcm files in the folder.
    """
    dcm_filepaths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".dcm"):
                dcm_filepaths.append(os.path.join(root, file))
    return dcm_filepaths

subfolders = get_subfolder_paths(ParentDirectory)

# Initialize an empty dictionary
data_dict = {}

def collectscores(seriesuid, scores):
    global data_dict

    keys = ['seriesuid name', 'year1', 'year2', 'year3', 'year4', 'year5', 'year6']
    values = [
        os.path.basename(seriesuid),
        scores[0][0][0],
        scores[0][0][1],
        scores[0][0][2],
        scores[0][0][3],
        scores[0][0][4],
        scores[0][0][5]
    ]

    # Use the seriesuid as the key for this entry in the data_dict
    entry_key = os.path.basename(seriesuid)
    data_dict[entry_key] = dict(zip(keys, values))

    return data_dict

def save_data_as_csv(data_dict, output_filename):

    # First, create an empty CSV file
    with open(output_filename, "w", newline='') as csvfile:
        pass

    # Open a CSV file in write mode
    with open(output_filename, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header row
        writer.writeheader()

        # Iterate over the data dictionary and write each entry to the CSV file
        for series_key, series_value in data_dict.items():
            writer.writerow(series_value)

def log_error(error_message, subfolder):
    with open(log_file, "a") as log:
        log.write("Error in subfolder '{}': {}\n".format(subfolder, error_message))
        traceback.print_exc(file=log)
subfolders = get_subfolder_paths(ParentDirectory)

headers = ["seriesuid name", "year1", "year2", "year3", "year4", "year5", "year6"]

for subfolder in subfolders:
    try:
        dcm_filepaths = get_dcm_filepaths(subfolder)
        serie = Serie(dcm_filepaths)
        scores = model.predict([serie])
        print(scores)
        folder_type = os.path.basename(os.path.normpath(ParentDirectory))
        data_dict = collectscores(subfolder, scores)
        save_data_as_csv(data_dict, csvoutput)
    except Exception as e:
        log_error(str(e), subfolder)
        continue

end_time_model = time.time()
print(f"Time taken for my_function: {end_time_model - start_time_model} seconds")