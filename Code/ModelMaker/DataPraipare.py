import os
import sys
from typing import Dict, List
import random
import logging
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np

sys.path.insert(0, r'Code\DataMaker')
from SignalGenerator import signal_functions, noise_beta



wanded_noise_levels = { 
            "Rauschen_25" : .25, 
            "Rauschen_50" : .5, 
            "Rauschen_75" : 0.75, 
            "Rauschen_100" :1}


def gen_dir_dict(data_dir: str, attribute: str, noise_type=None) -> Dict[str, List[str]]:
    """ Generate a dictionary of file paths based on specified attributes.

    Args:
        data_dir (str): Root directory for data
        attribute (str): Attribute for data selection ('cluster' or 'regression')
        noise_type (_type_, optional): Type of noise (default is None)(selection 'cluster'. 'Rot', 'Weis', 'Rosa')

    Raises:
        ValueError: Invalid attribute. Use 'Rot', 'Weis', 'Rosa'"
        ValueError: Invalid attribute. Use 'cluster' or 'regression'

    Returns:
        Dict[str, List[str]]: Dictionary mapping labels to lists of file paths
    """
    file_path_dict = {}
    path_dict = {}
    for dirpath, dirnames, filenames in os.walk(data_dir):
        for dirname in dirnames:
            wanted_dir = os.path.join(dirpath, dirname)
            if attribute == 'cluster':
                for noise_type in noise_beta:
                    if noise_type in wanted_dir:
                        for noise_level_name in wanded_noise_levels:
                            if wanded_noise_levels[noise_level_name] != 0 and noise_level_name in wanted_dir:
                                label_key = f"{noise_type}"
                                if label_key not in file_path_dict:
                                    file_path_dict[label_key] = []
                                for _, _, filenames in os.walk(wanted_dir):
                                    for filename in filenames:
                                        if filename.endswith('.csv'):
                                            file_dir = os.path.join(wanted_dir, filename)
                                            file_path_dict[label_key].append(file_dir)

                no_noise_label_key = "no_noise"
                no_noise_dir = r"Daten\Trainingsdaten\Ansauglufttemperatur\Rosa\Rauschen_0"
                no_noise_dict = {no_noise_label_key: []}

                for _, _, no_noise_filenames in os.walk(no_noise_dir):
                    for no_noise_filename in no_noise_filenames:
                        if no_noise_filename.endswith('.csv'):
                            no_noise_file_dir = os.path.join(no_noise_dir, no_noise_filename)
                            no_noise_dict[no_noise_label_key].append(no_noise_file_dir)

                path_dict = file_path_dict
                
            elif attribute == 'regression':
                if noise_type in ['Rot', 'Weis', 'Rosa']:
                    for dirname in dirnames:
                        if noise_type.capitalize() in dirname:
                            wanted_dir = os.path.join(dirpath, dirname)
                            for noise_level_name in wanded_noise_levels:
                                dir_path = os.path.join(wanted_dir, noise_level_name)

                                if noise_level_name in dir_path:
                                    label_key = wanded_noise_levels[noise_level_name]
                                    if label_key not in file_path_dict:
                                        file_path_dict[label_key] = []

                                    for _, _, filenames in os.walk(dir_path):
                                        for filename in filenames:
                                            if filename.endswith('.csv'):
                                                file_dir = os.path.join(dir_path, filename)
                                                file_path_dict[label_key].append(file_dir)

                    path_dict = file_path_dict

                else:
                    raise ValueError("Invalid attribute. Use 'Rot', 'Weis', 'Rosa'")  
            else:
                raise ValueError("Invalid attribute. Use 'cluster' or 'regression'.")
    log_sel_path(path_dict, 0)
    return path_dict


# logging
def log_sel_path(file_path_dict, sw):
    ''' Log selected file paths.
    Parameters:
    - file_path_dict: Dictionary mapping labels to lists of file paths.
    - sw: Switch for logging (True to log, False to skip).
    '''
    if sw == 1:
        log_filename = r'Dokumentation\logs\TreainigsdatenAuswahl.log'
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        for key, value in file_path_dict.items():
            logging.info(f"Key: {key}, Number of Elements: {len(value)}")
            for file_path in value:
                logging.info(f" 1 {file_path}")          
        print(f"Log written to {log_filename}")
    else: 
        print(f"No Log written.")
    
    
def red_file_path_dict(path_dict, ratio):
    """
    Reduce the number of file paths based on a specified ratio.

    Parameters:
    - path_dict: Dictionary mapping labels to lists of file paths.
    - ratio: Reduction ratio for the number of elements.

    Returns:
    - red_file_path_dict: Reduced dictionary of file paths.
    """
    num_random_elements = int(min(len(value) for value in path_dict.values())*ratio)
    red_file_path_dict ={}
    for key, value in path_dict.items():
        random_elements = random.sample(value, num_random_elements)
        if key not in red_file_path_dict:
            red_file_path_dict[key] = []
            for file_path in random_elements:
                red_file_path_dict[key].append(file_path)
    log_sel_path(red_file_path_dict, True)
    return red_file_path_dict
    
    
def label_data(data, path_dict):
    '''Label data with corresponding noise levels.

    Parameters:
    - data: DataFrame containing signal data.
    - path_dict: Dictionary mapping labels to lists of file paths.

    Returns:
    - labeled_data: pandas DataFrame with added labels.
    '''
    df = []
    for key in path_dict:
        label = noise_beta[key]
        print(label)
        for n in range(len(path_dict[key])):
            data_row = data[n]
            data_row['label'] = label  # Fix the typo here
            df.append(data_row)
    return pd.DataFrame(df)


def from_file_to_data(path_dict):
    """
    Load data from file paths into a list of DataFrames.

    Parameters:
    - path_dict: Dictionary mapping labels to lists of file paths.

    Returns:
    - data: List of DataFrames containing signal data.
    """
    
    data_frames = []
    for key, value in path_dict.items():
        print(f"Label: {key}, Type: {type(key)}, Key: {noise_beta[key]}")
        for path in value:
            print
            df = pd.read_csv(path)
            new_df = pd.DataFrame({noise_beta[key]: df['signal'].values + df['time'].values})
            data_frames.append(new_df)
    all_data = pd.concat(data_frames, axis=1)
    trans_data=all_data.transpose()
    df_cleaned = trans_data.dropna(axis=1)
    df_named = df_cleaned.rename_axis("label").reset_index()
    print(df_named)
    return df_named





