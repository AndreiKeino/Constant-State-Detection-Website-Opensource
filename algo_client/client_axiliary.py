#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 06:52:23 2026

@author: andrei
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

try:
    from models import (MAX_CSD_POINTS_FREE, CSD_Data, TestItem, 
                    to_jsonable_dict)
except:
    from csd_algo.models import (MAX_CSD_POINTS_FREE, CSD_Data, TestItem, 
                    to_jsonable_dict)


import sys
from typing import Literal


__version__: Literal[str] = '0.01'


def print_info(lst: list[str], msg_start: str='', 
               msg_finish: str = '') -> None:
    """
    axiliary function
    """
    print()
    print(msg_start)
    print()
    for e in lst:
        print(e)
        print()
    if len(msg_finish) > 0:
        print()
        print(msg_finish)
    

def report_results(out_data: CSD_Data, chart_title: str = '') -> None:  
    """
    function to report the results from the server's
    constant section detection routine
    """
    if len(out_data.csd_algo_errors) > 0:
        print_info(out_data.csd_algo_errors, 
                   f'got {len(out_data.csd_algo_errors)} error(s):',
                   'Please fix the error(s) and try again')
        return
    
    if len(out_data.csd_algo_warnings) > 0:
        print_info(out_data.csd_algo_warnings, 
                   f'got {len(out_data.csd_algo_warnings)} warnings(s):',
                   )
                
    
    y = out_data.csd_algo_input
    start = out_data.start
    finish = out_data.finish
    sss = out_data.start_section_series
    fss = out_data.finish_section_series
    
    print(f'lengh of start = {len(start)}')
    print(f'lengh of finish = {len(finish)}')
    
    print(f'lengh of start section series = {len(sss)}')
    print(f'lengh of finish section series = {len(fss)}')
    
    
    plot_results(y, start, finish,
                 sss,
                 fss, chart_title)
    
    print()
    print('start and finish constant state section index inclusive:')
    for i in range(len(start)):
        print(f'{start[i]}\t{finish[i]}')
        
    print()
    print(f'start and finish continuous constant state section series index inclusive:')
    for i in range(len(sss)):
        print(f'{sss[i]}\t{fss[i]}')
    
    if len(out_data.csd_algo_info) > 0:
        print_info(out_data.csd_algo_info, 
                   'Information:',
                   )
    

def plot_results(yy: list[float], 
                 start: list[int], 
                 finish: list[int], 
                 start_section_series: list[int], 
                 finish_section_series: list[int], 
                 chart_title: str) -> None:
    """
    function to plot the result of the constant series detection
    algorithm
    """
    y = np.array(yy)
    y_min = np.min(y)
    y_max = np.max(y)
    y_mid = (y_max + y_min) / 2.0
    
    
    x = np.arange(len(y))
    fig, ax = plt.subplots()
    plt.plot(x, y, 
             color='b', 
             label='input data')

    lbl = 'constant state section'
    for i in range(len(start)):
        label = lbl if i == 0 else None
        rect = patches.Rectangle(
            (start[i], y_mid), 
            finish[i] - start[i], 
            y_max - y_mid, 
            linewidth=1, edgecolor='r', facecolor='g', 
            alpha = 0.16, label=label)
        ax.add_patch(rect)
        
    sss = start_section_series
    fss = finish_section_series
    
    lbl = 'continuous constant state section series'
    
    for i in range(len(sss)):
        label = lbl if i == 0 else None
        rect = patches.Rectangle(
            (sss[i], y_min), 
            fss[i] - sss[i], 
            y_mid - y_min, 
            linewidth=1, edgecolor='g', facecolor='r', 
            alpha = 0.16, label=label)
        ax.add_patch(rect)        
    
    plt.hlines(y_mid, 0, len(y) - 1, color='g')
    title: str = (chart_title if len(chart_title) > 0 
                  else 'Constant State Detection algorithm results')
    plt.title(title)
    plt.xlabel('index')
    plt.ylabel('data')
    plt.legend()
    
    
    plt.show()
