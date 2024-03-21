import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import SimpleITK as sitk
import pandas as pd

# canal rouge
# a = -6.2517E-13
# b = 6.5866E-08
# c = - 2.4741E-03
# d = 3.3246E+01
a = -2.6408E-13
b = 3.3382E-8
c = 1.5142E-3
d = 23.846

def etalonnage_X23(x):
    return a*x**3 + b*x**2 + c*x + d

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
        img_arr0 = sitk.GetArrayFromImage(sitk.ReadImage(str(tiff_files[0])))[400:800, 200:600]
        img_arr1 = sitk.GetArrayFromImage(sitk.ReadImage(str(tiff_files[1])))[400:800, 200:600]
        img_arr2 = sitk.GetArrayFromImage(sitk.ReadImage(str(tiff_files[2])))[400:800, 200:600]
        lim_inf_vertical = np.where(img_arr0 < 30000)
        lim_sup_vertical = np.where(img_arr0 < 30000)[1][0]
        plt.imshow(img_arr0)
        # plt.axhline(lim_inf_vertical)
        # plt.axvline(lim_sup_vertical)
        plt.colorbar()
        plt.show()
    img_arr_mean = np.mean([img_arr0[520:600, 400:475].mean(), img_arr1[520:600, 400:475].mean(), img_arr2[520:600, 400:475].mean()])

    mean.append(img_arr_mean)

# data = [date, hour, mean]
# df = pd.DataFrame.from_records(data).T
# df.columns = ['Date', 'Heure', 'PV']
# date_hour = []
# for i in range(len(df)):
#     date_hour.append(df.iloc[i, 0][:4] + '/' + df.iloc[i, 0][4:6] + '/' + df.iloc[i, 0][6:] + ' ' + df.iloc[i, 1][:2] + ':' + df.iloc[i, 1][2:4])

# df['Date et heure'] = date_hour
# df['Date et heure'] = pd.to_datetime(df['Date et heure'])
# df['Durée (h)'] = pd.to_numeric((df['Date et heure'] - pd.to_datetime(initial_date)) / (1E9 * 3600))
# df['Dose (Gy)'] = etalonnage_X23(df['PV'])
# df['Ecart dose (%)'] = (df['Dose (Gy)'] - 1.999) / 1.999 * 100

# plt.figure(figsize=(12, 7))
# plt.scatter(df['Durée (h)'], df['Dose (Gy)'], marker='x')
# plt.xlabel('Durée (h)')
# plt.ylabel('Dose (Gy)')
# plt.title('Effet de fading')
# plt.grid(ls='--')
# plt.show()
