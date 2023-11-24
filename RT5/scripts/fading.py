import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import SimpleITK as sitk
import pandas as pd

tiff_files = list(Path('/Volumes/LEXAR/fading/new_tiff/').rglob('*.tif'))
time = [str(f).split('/')[5] for f in tiff_files][::3]
initial_date = '2023/11/15 09:14:00'

mean = []
date = []
hour = []
for t in time:
    tiff_files = list(Path('/Volumes/LEXAR/fading/new_tiff/' + t).glob('*.tif'))
    date.append(str(tiff_files[0]).split('_')[3])
    hour.append(str(tiff_files[0]).split('_')[4])
    for tiff in tiff_files:
        img_arr0 = 2**16 - sitk.GetArrayFromImage(sitk.ReadImage(str(tiff_files[0])))[520:600, 400:475].mean()
        img_arr1 = 2**16 - sitk.GetArrayFromImage(sitk.ReadImage(str(tiff_files[1])))[520:600, 400:475].mean()
        img_arr2 = 2**16 - sitk.GetArrayFromImage(sitk.ReadImage(str(tiff_files[2])))[520:600, 400:475].mean()
    img_arr_mean = np.mean([img_arr0, img_arr1, img_arr2])

    mean.append(img_arr_mean)

data = [date, hour, mean]
df = pd.DataFrame.from_records(data).T
df.columns = ['Date', 'Heure', 'Moyenne pixel']
date_hour = []
for i in range(len(df)):
    date_hour.append(df.iloc[i, 0][:4] + '/' + df.iloc[i, 0][4:6] + '/' + df.iloc[i, 0][6:] + ' ' + df.iloc[i, 1][:2] + ':' + df.iloc[i, 1][2:4])

df['Date et heure'] = date_hour
df['Date et heure'] = pd.to_datetime(df['Date et heure'])
df['Durée (h)'] = (df['Date et heure'] - pd.to_datetime(initial_date)) / (1E9 * 3600)
df['Dose (Gy)'] = df['Moyenne pixel'] * 2 / df['Moyenne pixel'].to_list()[-1]

plt.figure(figsize=(12, 7))
plt.scatter(df['Durée (h)'], df['Dose (Gy)'], marker='x')
plt.xlabel('Durée (h)')
plt.ylabel('Dose (Gy)')
plt.title('Effet de fading')
plt.grid(ls='--')
plt.ylim(1.9, 2.025)
plt.show()
print(df)