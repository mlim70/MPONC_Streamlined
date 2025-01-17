#save_values.py

import pickle
from pathlib import Path

def save_current_values(id_list, file_path):
    """ Save current ID's to cache """
    with open(file_path, 'wb') as file:
        pickle.dump(id_list, file)
    print(f"Current ID's saved.\n")

def load_previous_values(file_path):
    """ Load previous ID's from cache """
    if Path(file_path).exists(): # If exists
        with open(file_path, 'rb') as f:
            saved_IDS = pickle.load(f)
    else: # Initialize empty array
        saved_IDS = []
    return saved_IDS