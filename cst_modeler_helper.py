from typing import List, Tuple
import cst
import cst.interface

metal_thickness = 0.035 # mm

copper_pure = 'Copper (pure)'

def define_components(modeler, component_names: List):
    # Theoretically there should be a existance check, but now it is unclear 
    # how to retrieve CST VBA outputs via Python
    for component_name in component_names:
        s_new_component = f'Component.New "{component_name}"'
        modeler.add_to_history(f'add new component: {component_name}', s_new_component)

def delete_components(modeler, component_names: List):
    # Theoretically there should be a existance check, but now it is unclear 
    # how to retrieve CST VBA outputs via Python
    for component_name in component_names:
        s_delete_component = f'Component.Delete "{component_name}"'
        modeler.add_to_history(f'delete component: {component_name}', s_delete_component)

def define_brick(modeler,
                 brick_name: str, component_name: str, material: str, 
                 x_range: Tuple, y_range: Tuple, z_range: Tuple):
    
    s_brick = ['With Brick',
               '.Reset',
               f'.Name "{brick_name}"',
               f'.Component "{component_name}"',
               f'.Material "{material}"',
               f'.Xrange "{x_range[0]}", "{x_range[1]}"',
               f'.Yrange "{y_range[0]}", "{y_range[1]}"',
               f'.Zrange "{z_range[0]}", "{z_range[1]}"',
               '.Create',
               'End With']
    s_brick = '\n'.join(s_brick)
    modeler.add_to_history(f'define brick:{component_name}:{brick_name}', s_brick)