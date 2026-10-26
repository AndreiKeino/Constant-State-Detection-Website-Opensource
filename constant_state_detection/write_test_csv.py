import numpy as np
import pandas as pd

points = 1024 * 1024 # 128 256 264 512
periods = 1

x: np.ndarray = np.arange(points)
y: np.ndarray = np.sin(2.0 * np.pi * periods * x / points)

df = pd.DataFrame({'Column1': y,})
file_name = f'{points}_points_{periods}_periods.csv'
df.to_csv(file_name, header=False, index=False)




