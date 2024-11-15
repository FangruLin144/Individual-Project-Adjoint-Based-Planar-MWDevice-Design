import numpy as np
from scipy.ndimage import gaussian_filter1d

def average_window(data, window_size: int=5):
    data_length = len(data)

    window = []
    data_new = []
    for i in range(data_length):
        window.append(data[i])
        if i >= window_size: 
            del window[0]
        y_value_new = np.average(window)
        data_new.append(y_value_new)
    
    return np.array(data_new)

def gaussian_filter(data, sigma: float=5.0):
    data_new = gaussian_filter1d(data, sigma)
    return data_new