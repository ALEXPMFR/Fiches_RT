import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import SimpleITK as sitk

tiff_files = sorted(list(Path('/Volumes/LEXAR/fading/tiff_bruts').rglob('*.tif')))

for tiff in tiff_files:
    img = sitk.ReadImage(str(tiff))
    img_arr = sitk.GetArrayFromImage(img)[:, :, 0]
    new_img = sitk.GetImageFromArray(img_arr)
    sitk.WriteImage(new_img, '/Volumes/LEXAR/fading/new_tiff/' + str(tiff).split('/')[5] + '/' + str(tiff).split('/')[-1])
    