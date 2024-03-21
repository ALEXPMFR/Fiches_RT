# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:51:24 2022

@author: s-chiavassa

Il faut avoir réalisé 3 scanners identiques (RGB .TIFF) d'un même film an les nommant xxx_01.tiff, xxx_02.tiff et xxx_03.tiff
--> notation automatique de l'epson avec incrément à 2 chiffres.

Ce script converti la moyenne des 3 scanners (TIFF RGB 48 bits) d'un film en dose selon le canal rouge ou vert.
Passage sur le canal vert pour des doses > 5Gy

"""

import numpy as np
import tifffile as tiff
import tkinter
from tkinter import *
import tkinter.filedialog as fd
import os.path

# demande à l'utilisateur d'ouvrir un des 3 fichiers du film scanné #############################################
file = fd.askopenfilename(title='Choose a file of any type', filetypes=[("All files", "*.*")])

# récupération des 3 fichiers. Extraction du rouge et du vert. Conversion en matrice et calcul de la matrice de PV mean  #############################################
#print (file)
#print (len(file))
#print (file[0:len(file)-5])

file1 = file
file2 = file[0:len(file)-5] + '2.tif'
file3 = file[0:len(file)-5] + '3.tif'

# # position de l'isocentre (en pixel)  #############################################

# Y_gauche = 350
# Y_droite = 351
# X_haut = 380
# X_bas = 379


Y_gauche = 592
Y_droite = 592
X_haut = 374
X_bas = 374

'''
Y_gauche = 592
Y_droite = 591
X_haut = 361
X_bas = 360
'''

# coordonnées de l'isocentre
Y_mean = int((Y_gauche + Y_droite)/2)
X_mean = int((X_haut + X_bas)/2)
#print (X_mean, Y_mean)

# calcul des bornes pour cropper l'image autour de l'isocentre 
# on prend l'isocentre +/- la motier du film - 2cm  (1cm de chaque coté)
# comme ça on est sur que l'isocentre est bien au centre de l'image
Y_inf = Y_mean - 345
Y_sup = Y_mean + 345
X_sup = X_mean + 272
X_inf = X_mean - 272


# ouverture des 3 images #############################################
img1 = tiff.imread(file1)
img2 = tiff.imread(file2)
img3 = tiff.imread(file3)

# extraction du canal rouge
img1_red = img1[:,:,0]
img2_red = img2[:,:,0]
img3_red = img3[:,:,0]

# extraction du canal vert
img1_green = img1[:,:,1]
img2_green = img2[:,:,1]
img3_green = img3[:,:,1]


# crop des images
img1_red_crop = img1_red[Y_inf:Y_sup,X_inf:X_sup]
img2_red_crop = img2_red[Y_inf:Y_sup,X_inf:X_sup]
img3_red_crop = img3_red[Y_inf:Y_sup,X_inf:X_sup]
img1_green_crop = img1_green[Y_inf:Y_sup,X_inf:X_sup]
img2_green_crop = img2_green[Y_inf:Y_sup,X_inf:X_sup]
img3_green_crop = img3_green[Y_inf:Y_sup,X_inf:X_sup]


# transformation en matrice
imarray1_red = np.array(img1_red_crop)
imarray2_red = np.array(img2_red_crop)
imarray3_red = np.array(img3_red_crop)
imarray1_green = np.array(img1_green_crop)
imarray2_green = np.array(img2_green_crop)
imarray3_green = np.array(img3_green_crop)

# création de la matrice moyenne
rows = imarray1_red.shape[0]
cols = imarray1_red.shape[1]
imarray_moyenne_red = np.zeros((rows, cols))
imarray_moyenne_green = np.zeros((rows, cols))

for i in range(0, rows-1):
    for j in range(0, cols-1):
        imarray_moyenne_red[i,j] = (imarray1_red[i,j]/3) + (imarray2_red[i,j]/3) + (imarray3_red[i,j]/3)
        imarray_moyenne_green[i,j] = (imarray1_green[i,j]/3) + (imarray2_green[i,j]/3) + (imarray3_green[i,j]/3)
        



# coefficient des courbes d'étalonnage de type polynômes de degré 3  #############################################

# de 0 à 5Gy  (PV limite = 19100) >>> red
a1_red = -4.451e-13
b1_red = 5.121e-8 
c1_red = -2.045e-3
d1_red = 28.49


# de > 5  à 25Gy   >>>  green
a2_green = -6.697e-12
b2_green = 4.217e-7
c2_green = -9.657e-3
d2_green = 84.40



#○ application des polynomes de degré 3 selon la courbe #############################################
imarray_dose = np.zeros((rows, cols))

for i in range(0, rows-1):
    for j in range(0, cols-1):
#        print (imarray_moyenne_red[i,j])
        if imarray_moyenne_red[i,j] > 19100:
            imarray_dose[i,j] = (a1_red*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j])+(b1_red*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j])+(c1_red*imarray_moyenne_red[i,j])+d1_red
#            print ('sup')
#            print (imarray_dose[i,j])
        else:
            imarray_dose[i,j] = (a2_green*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j])+(b2_green*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j])+(c2_green*imarray_moyenne_green[i,j])+d2_green
#            print ('inf')
#            print (imarray_dose[i,j])
            

# sauvegarde de la matrice de dose #############################################

#print (imarray[0,0])
imarray_dose = abs(np.float32(imarray_dose))
print(imarray_dose)
resolution_mm = 2.54/75

print(type(imarray_dose))
print(np.shape(imarray_dose))

#print (imarray_dose[0,0])
#tiff.imshow(imarray_dose)
# tiff.imsave(file[0:len(file)-6] + 'dose_RG_test_abs.tiff', imarray_dose, resolution=(1/resolution_mm, 1/resolution_mm , 'CENTIMETER'))
print ('done')

