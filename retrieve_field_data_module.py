import numpy as np
import h5py

def find_exact_index(array, value):
    # Find the index where the value exactly matches
    idx = np.where(array == value)[0]
    if len(idx) == 0:
        raise ValueError(f"Value {value} not found in array")
    return idx[0]

def find_nearest_index(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or np.abs(value - array[idx-1]) < np.abs(value - array[idx])):
        return idx-1
    else:
        return idx
    
def find_field_data_of_interest(file_path: str, coordinates, type: str):
    with h5py.File(file_path, 'r') as f:
        field_data = f[type][:]
        position = f['Position'][:]

    x_position = position['x']
    y_position = position['y']
    unique_x = np.unique(x_position)
    unique_y = np.unique(y_position)
    field_data_reshape = field_data.reshape(len(unique_y), len(unique_x))

    field_complex_values = []
    for coord in coordinates: 
        x, y = coord
        x_idx = find_nearest_index(unique_x, x)
        y_idx = find_nearest_index(unique_y, y)
        x_complex = field_data_reshape['x']['re'][y_idx, x_idx] + 1j * field_data_reshape['x']['im'][y_idx, x_idx]
        y_complex = field_data_reshape['y']['re'][y_idx, x_idx] + 1j * field_data_reshape['y']['im'][y_idx, x_idx]
        z_complex = field_data_reshape['z']['re'][y_idx, x_idx] + 1j * field_data_reshape['z']['im'][y_idx, x_idx]

        field_complex_values.append(np.array([x_complex, y_complex, z_complex]))

    # Return a list of numpy arrays, with each array containing the complex components of the field
    return field_complex_values