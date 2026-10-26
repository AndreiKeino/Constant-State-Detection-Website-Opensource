#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

import matplotlib.pyplot as plt
import matplotlib.patches as patches

try:
    from client_axiliary import report_results, __version__
    from models import (MAX_CSD_POINTS_FREE, CSD_Data, TestItem, 
                        AlgorithmType, WindowHeightType, 
                        to_jsonable_dict)

    from generate_timeseries_numpy import generate_timseries
except Exception:
    from csd_algo.client_axiliary import report_results, __version__
    from csd_algo.models import (MAX_CSD_POINTS_FREE, CSD_Data, TestItem, 
                        AlgorithmType, WindowHeightType, 
                        to_jsonable_dict)
    from csd_algo.generate_timeseries_numpy import generate_timseries


plt.close('all')
 
url_csd_algo = 'https://dazzling-faithful-banteng.anvil.app/constant-state-detection'
''

# url_csd_algo = 'https://reflex-csd-app-navy-grass.reflex.run:8000/api/constant-state-detection'
# create the timeseries to be processed:
    
ts: list[float] = generate_timseries(
    0.5, 
    MAX_CSD_POINTS_FREE,
    ).tolist()

# process the timeseries with the default settings:
    
csd_data = CSD_Data(csd_algo_input=ts, 
                    csd_algo_min_window_width=16, 
                    csd_algo_max_window_height=0.08)

# send the data to the server and receive the reply
response = requests.post(url_csd_algo, 
                         json=to_jsonable_dict(csd_data))

# validate received data
out_data = CSD_Data.model_validate(response.json())

# print and plot the processing results
report_results(out_data, 
               f'CSD plot, Algorithm type: postprocessing')


# do the same using AlgorithmType.ALGO_WITHOUT_POSTPROCESSING setting
         
csd_data.Algo_Type = AlgorithmType.ALGO_WITHOUT_POSTPROCESSING

response = requests.post(url_csd_algo, 
                         json=to_jsonable_dict(csd_data))

print('response status code:\n', response.status_code)
out_data = CSD_Data.model_validate(response.json())

report_results(out_data, 
               f'CSD plot: Algorithm type: simple')


print(f'Package version: {__version__}')




