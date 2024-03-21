import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import SimpleITK as sitk

tif_files = list(Path('/Volumes/LEXAR/Fiches_DQ/RT/RT5/rdm_X23/').glob('*v*.tif'))
mean_arr = np.zeros([918-328, 8])
for i in tif_files:
    img_arr = sitk.GetArrayFromImage(sitk.ReadImage(str(i)))[:, :, 0][328:918, 392:400]
    mean_arr += img_arr
    pixel_spacing = sitk.ReadImage(str(i)).GetSpacing()[0]

mean_arr /= 3
rdt = np.zeros([1, mean_arr.shape[0]])
for i in range(mean_arr.shape[1]):
    rdt += mean_arr[:, i]

rdt = rdt[0] / mean_arr.shape[1]

# canal rouge
a = -6.2517E-13
b = 6.5866E-08
c = - 2.4741E-03
d = 3.3246E+01

def etalonnage_X23(x):
    return a*x**3 + b*x**2 + c*x + d

numbre_pixel = [f for f in range(mean_arr.shape[0])]
depth = [f * pixel_spacing for f in numbre_pixel]
data = [depth, rdt]

df = pd.DataFrame.from_records(data).T
df.columns = ['Profondeur (mm)', 'PV']
df['Dose (Gy)'] = etalonnage_X23(df['PV'])
df['Dose normalisée (%)'] = df['Dose (Gy)'] / df['Dose (Gy)'].max() * 100
plt.figure(figsize=(12, 7))
plt.plot(df['Profondeur (mm)'], df['Dose normalisée (%)'])
plt.grid(ls='--')
plt.xlabel('Profondeur (mm)')
plt.ylabel('Dose relative (%)')
plt.title('Rendement en profondeur X23 film')
plt.show()

# tif_files = list(Path('/Volumes/LEXAR/Fiches_DQ/RT/RT5/rdm_X23/').glob('*h*.tif'))
# img_arr = sitk.GetArrayFromImage(sitk.ReadImage(str(tif_files[0])))[:, :, 0][603:615, 118:710]

# mean_arr = np.zeros([615-605, 700-125])
# for i in tif_files:
#     img_arr = sitk.GetArrayFromImage(sitk.ReadImage(str(i)))[:, :, 0][605:615, 125:700]
#     mean_arr += img_arr
#     pixel_spacing = sitk.ReadImage(str(i)).GetSpacing()[0]

# mean_arr /= 3
# mean_arr = - mean_arr
# rdt_2 = np.zeros([1, mean_arr.shape[1]])
# for i in range(mean_arr.shape[0]):
#     rdt_2 += mean_arr[i, ::-1]

# rdt_2 /= mean_arr.shape[0]
# rdt_2 /= rdt_2.max() / 100
# plt.plot([f * pixel_spacing for f in range(rdt.shape[1])], rdt[0], label='Vertical')
# plt.plot([f * pixel_spacing for f in range(rdt_2.shape[1])], rdt_2[0], label='Horizontal')
# plt.legend()
# plt.show()