# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 10:30:31 2021

@author: Andrei
"""

# import pandas as pd

import numpy as np

def generate_timseries(b: float, points_cnt: int=256, 
                       periods: int=1, 
                       phi: float = 0) -> np.array:
        """
        function to generate the test timeseries for the 
        constant state detection algorithm demo. returns the 
        float numpy array with the sin(x) + b * sin(2 * x + phi)
        sum of the first and the second harmonic inside.

        input parameters:
        * b - float, the value of the second harmonic
        * points_cnt - int, the count of the points in the output array
        * periods - int, the period count of the first harmonic
        * phi - float, the phase of the second harmonic in the PI * radians 

        """

        points = int(periods * points_cnt)
        phase = phi * np.pi
        x = np.arange(points)
        y = np.sin(2.0 * np.pi * periods * x / points)
        sin2 = b * np.sin(4.0 * np.pi * periods * x / points + phase)
        y += sin2
        return y
    


