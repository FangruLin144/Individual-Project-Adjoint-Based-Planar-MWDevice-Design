import pickle
import os
import h5py
from datetime import datetime
import numpy as np

def generate_file(base_path) -> str:
        new_path = f"coordinate_history/{base_path}.hdf5"
        return new_path

def list_datasets(file_name): 
    with h5py.File(file_name, 'r') as f:
        print(f"File name:\t{file_name}\n")
        print(f"Metadata of the file:")
        for attr_name, attr_value in f.attrs.items():
            print(f"\t{attr_name}:\t{attr_value}")
        print()
        print(f"Datasets in the file:")
        for key in f:
            if isinstance(f[key], h5py.Dataset): 
                print(f"\t{key}")

def save_data(file_name, description, coordinates): 
    if os.path.exists(file_name): os.remove(file_name)

    with h5py.File(file_name, 'w') as f:
        creation_time = datetime.now().isoformat()
        f.attrs['creation_time'] = creation_time
        f.attrs['description'] = description

        coord_pickle = pickle.dumps(coordinates)
        f.create_dataset('coordinates', data=np.void(coord_pickle))

def retrieve_dataset(file_name, dataset_name): 
    with h5py.File(file_name, 'r') as f:
        dataset_pickle = f[dataset_name][()]
        dataset = pickle.loads(dataset_pickle.tobytes())

        return dataset