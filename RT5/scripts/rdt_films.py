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
mean_arr = - mean_arr
rdt = np.zeros([1, mean_arr.shape[0]])
for i in range(mean_arr.shape[1]):
    rdt += mean_arr[:, i]

rdt /= mean_arr.shape[0]
rdt /= rdt.max() / 100
plt.plot([f * pixel_spacing for f in range(rdt.shape[1])], rdt[0])
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