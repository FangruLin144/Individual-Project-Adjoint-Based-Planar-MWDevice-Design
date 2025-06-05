import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from scipy.interpolate import CubicSpline
    
def coordinates_init(params):
    coords = []
    for param in params: 
        x_min, x_max, y_min, y_max, step_size, axis = param
        
        if axis == 1: 
            x = np.arange(x_min, x_max, step_size)
            y_ub = y_max * np.ones_like(x)
            y_lb = y_min * np.ones_like(x)
            coords.append((x, y_ub, y_lb))
        else:
            y = np.arange(y_min, y_max, step_size)
            x_ub = x_max * np.ones_like(y)
            x_lb = x_min * np.ones_like(y)
            coords.append((y, x_ub, x_lb))
    return coords

def find_coordinate_shape(params):
    lengths = []
    lengths.extend(len(param[0]) for param in params)
    return len(params), lengths

def coordinates_flatten(params, axis): 
    coords_shape = find_coordinate_shape(params)

    coords = []
    for i, param in enumerate(params):
        if axis[i] == 1: 
            x, y_ub, y_lb = param
            length = len(x)
            coords.extend((x[j], y_ub[j]) for j in range(length))
            coords.extend((x[j], y_lb[j]) for j in range(length))
        else: 
            y, x_ub, x_lb = param
            length = len(y)
            coords.extend((x_ub[j], y[j]) for j in range(length))
            coords.extend((x_lb[j], y[j]) for j in range(length))
    
    return coords, coords_shape

def coordinates_resemble(coordinates, coords_shape, axis):
    section, lengths = coords_shape
    coords = []
    
    pos = 0
    for i in range(section):
        length = lengths[i]

        if axis[i] == 1: 
            x = np.array([coord[0] for coord in coordinates[pos:pos+length]])
            y_ub = np.array([coord[1] for coord in coordinates[pos:pos+length]])
            y_lb = np.array([coord[1] for coord in coordinates[pos+length:pos+length*2]])
            coords.append((x, y_ub, y_lb))
        else:
            y = np.array([coord[1] for coord in coordinates[pos:pos+length]])
            x_ub = np.array([coord[0] for coord in coordinates[pos:pos+length]])
            x_lb = np.array([coord[0] for coord in coordinates[pos+length:pos+length*2]])
            coords.append((y, x_ub, x_lb))

        pos += length * 2
    return coords

def coordinates_distribute(coordinates, axis):
    length = len(coordinates)

    if axis == 1:
        x = np.array([coordinates[i][0] for i in range(length)], dtype=object)
        y_ub = np.array([coordinates[i][1] for i in range(length)], dtype=object)
        y_lb = np.array([coordinates[i][2] for i in range(length)], dtype=object)
        return x, y_ub, y_lb
    else: 
        y = np.array([coordinates[i][0] for i in range(length)], dtype=object)
        x_ub = np.array([coordinates[i][1] for i in range(length)], dtype=object)
        x_lb = np.array([coordinates[i][2] for i in range(length)], dtype=object)
        return y, x_ub, x_lb
    

def plot_section(x, y, xlim: Tuple, ylim: Tuple, label: List, axis: int=1):
    salmon_red = '#FA8072'
    mint = '#40E0D0'
    blue = '#3F51B5'
    colors = [blue, salmon_red, mint, mint]

    plt.figure(figsize=(21,6))

    if axis == 1: 
        length = len(y)
        for i in range(length): plt.plot(x, y[i], label=label[i], color=colors[i])

        plt.legend()
        plt.xlabel('Position (mm)')
        plt.ylabel('Trace geometries (mm)')
        if xlim != None: plt.xlim(xlim[0], xlim[1])
        if ylim != None: plt.ylim(ylim[0], ylim[1])
    else: 
        length = len(x)
        for i in range(length): plt.plot(x[i], y, label=label[i], color=colors[i])

        plt.legend()
        plt.xlabel('Position (mm)')
        plt.ylabel('Trace geometries (mm)')
        if xlim != None: plt.xlim(xlim[0], xlim[1])
        if ylim != None: plt.ylim(ylim[0], ylim[1])

    plt.show()

def poly_fit_ends(x, y, pstart, pend, step_size, sample_rate, sample_distance):
    # Extend both ends of x and y (along x axis)
    x_extended = np.arange(pstart[0]-step_size, pend[0]+sample_rate*step_size, step_size)

    y_start = np.full(1, fill_value=pstart[1])
    y_end = np.full(sample_rate, fill_value=pend[1])
    y_extended = np.concatenate((y_start, y, y_end))

    # Sample x and y
    x_extended_start_sampled = x_extended[:sample_distance+sample_rate:sample_rate]
    x_extended_end_sampled = x_extended[-sample_distance-sample_rate::sample_rate]
    y_extended_start_sampled = y_extended[:sample_distance+sample_rate:sample_rate]
    y_extended_end_sampled = y_extended[-sample_distance-sample_rate::sample_rate]

    # Define CubicSpline objects for the start and the end
    cs_start = CubicSpline(x_extended_start_sampled, y_extended_start_sampled, bc_type='natural')
    cs_end = CubicSpline(x_extended_end_sampled, y_extended_end_sampled, bc_type='natural')

    # Interpolate y at the original step size
    y_start_interpolated = cs_start(x_extended[:sample_distance])
    y_end_interpolated = cs_end(x_extended[-sample_distance-sample_rate:-sample_rate])

    # Replace the original parts with fitted parts
    y[:sample_distance] = y_start_interpolated
    y[-sample_distance:] = y_end_interpolated

    return y