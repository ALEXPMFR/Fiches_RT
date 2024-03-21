o# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:51:24 2022

@author: s-chiavassa

Il faut avoir réalisé 3 scanners identiques (RGB .TIFF) d'un même film an les nommant xxx_01.tiff, xxx_02.tiff et xxx_03.tiff
--> notation automatique de l'epson avec incrément à 2 chiffres.
"""

import numpy as np
import tifffile as tiff
import tkinter
from tkinter import *
import tkinter.filedialog as fd
import os.path

# demande à l'utilisateur d'ouvrir un des 3 fichiers du film scanné #############################################
file = fd.askopenfilename(title='Choose a file of any type', filetypes=[("All files", "*.*")])

# récupération des 3 fichiers. Extraction du rouge. Conversion en matrice et calcul de la matrice de PV mean  #############################################
print (file)
print (len(file))
print (file[0:len(file)-5])

file1 = file
file2 = file[0:len(file)-5] + '2.tif'
file3 = file[0:len(file)-5] + '3.tif'

# position de l'isocentre (en pixel)  #############################################
Y_gauche = 592
Y_droite = 592
X_haut = 374
X_bas = 374

# coordonnées de l'isocentre
Y_mean = int((Y_gauche + Y_droite)/2)
X_mean = int((X_haut + X_bas)/2)
print (X_mean, Y_mean)

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

# extraction du canal bleu
img1_blue = img1[:,:,2]
img2_blue = img2[:,:,2]
img3_blue = img3[:,:,2]


# crop des images
img1_red_crop = img1_red[Y_inf:Y_sup,X_inf:X_sup]
img2_red_crop = img2_red[Y_inf:Y_sup,X_inf:X_sup]
img3_red_crop = img3_red[Y_inf:Y_sup,X_inf:X_sup]

img1_green_crop = img1_green[Y_inf:Y_sup,X_inf:X_sup]
img2_green_crop = img2_green[Y_inf:Y_sup,X_inf:X_sup]
img3_green_crop = img3_green[Y_inf:Y_sup,X_inf:X_sup]

img1_blue_crop = img1_blue[Y_inf:Y_sup,X_inf:X_sup]
img2_blue_crop = img2_blue[Y_inf:Y_sup,X_inf:X_sup]
img3_blue_crop = img3_blue[Y_inf:Y_sup,X_inf:X_sup]

# transformation en matrice
imarray1_red = np.array(img1_red_crop)
imarray2_red = np.array(img2_red_crop)
imarray3_red = np.array(img3_red_crop)

imarray1_green = np.array(img1_green_crop)
imarray2_green = np.array(img2_green_crop)
imarray3_green = np.array(img3_green_crop)

imarray1_blue = np.array(img1_blue_crop)
imarray2_blue = np.array(img2_blue_crop)
imarray3_blue = np.array(img3_blue_crop)

# création de la matrice moyenne
rows = imarray1_red.shape[0]
cols = imarray1_red.shape[1]
imarray_moyenne_red = np.zeros((rows, cols))
imarray_moyenne_green = np.zeros((rows, cols))
imarray_moyenne_blue = np.zeros((rows, cols))
for i in range(0, rows-1):
    for j in range(0, cols-1):
        imarray_moyenne_red[i,j] = (imarray1_red[i,j]/3) + (imarray2_red[i,j]/3) + (imarray3_red[i,j]/3)
        imarray_moyenne_green[i,j] = (imarray1_green[i,j]/3) + (imarray2_green[i,j]/3) + (imarray3_green[i,j]/3)
        imarray_moyenne_blue[i,j] = (imarray1_blue[i,j]/3) + (imarray2_blue[i,j]/3) + (imarray3_blue[i,j]/3)
        
imarray_moyenne_red = np.float32(imarray_moyenne_red)
imarray_moyenne_green = np.float32(imarray_moyenne_green)
imarray_moyenne_blue = np.float32(imarray_moyenne_blue)


# coefficient des courbes d'étalonnage de type polynômes de degré 4  #############################################

# de 0 à 5Gy  (PV limite = 19100) RED
a1_red = -4.451e-13
b1_red = 5.121e-8 
c1_red = -2.045e-3
d1_red = 28.49

# de > 5  à 25Gy  RED
a2_red = -1.415e-11
b2_red = 7.440e-7
c2_red = -1.39e-2
d2_red = 97.75


# de 0 à 5Gy  (PV limite = 19100) GREEN
a1_green = -4.733e-13
b1_green = 5.557e-8 
c1_green = -2.307e-3
d1_green = 33.73

# de > 5  à 25Gy  GREEN
a2_green = -6.697e-12
b2_green = 4.217e-7
c2_green = -9.657e-3
d2_green = 84.40

# de 0 à 5Gy  (PV limite = 19100) BLUE
a1_blue = -8.080e-13
b1_blue = 1.047e-7 
c1_blue = -4.319e-3
d1_blue = 56.76

# de > 5  à 25Gy  BLUE
a2_blue = -1.149e-11
b2_blue = 7.244e-7
c2_blue = -1.665e-2
d2_blue = 141.2



#○ application des polynomes de degré 4 selon la courbe RED #############################################
imarray_dose_red = np.zeros((rows, cols))
imarray_dose_green = np.zeros((rows, cols))
imarray_dose_blue = np.zeros((rows, cols))

for i in range(0, rows-1):
    for j in range(0, cols-1):
#        print (imarray_moyenne_red[i,j])
        if imarray_moyenne_red[i,j] > 19100:
            imarray_dose_red[i,j] = (a1_red*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j])+(b1_red*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j])+(c1_red*imarray_moyenne_red[i,j])+d1_red
#            print ('sup')
#            print (imarray_dos_red[i,j])
        else:
            imarray_dose_red[i,j] = (a2_red*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j])+(b2_red*imarray_moyenne_red[i,j]*imarray_moyenne_red[i,j])+(c2_red*imarray_moyenne_red[i,j])+d2_red
#            print ('inf')
#            print (imarray_dose_red[i,j])
        if imarray_moyenne_green[i,j] > 21000:
            imarray_dose_green[i,j] = (a1_green*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j])+(b1_green*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j])+(c1_green*imarray_moyenne_green[i,j])+d1_green
        else:
            imarray_dose_green[i,j] = (a2_green*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j])+(b2_green*imarray_moyenne_green[i,j]*imarray_moyenne_green[i,j])+(c2_green*imarray_moyenne_green[i,j])+d2_green
        if imarray_moyenne_blue[i,j] > 20000:
            imarray_dose_blue[i,j] = (a1_blue*imarray_moyenne_blue[i,j]*imarray_moyenne_blue[i,j]*imarray_moyenne_blue[i,j])+(b1_blue*imarray_moyenne_blue[i,j]*imarray_moyenne_blue[i,j])+(c1_blue*imarray_moyenne_blue[i,j])+d1_blue
        else:
            imarray_dose_blue[i,j] = (a2_blue*imarray_moyenne_blue[i,j]*imarray_moyenne_blue[i,j]*imarray_moyenne_blue[i,j])+(b2_blue*imarray_moyenne_blue[i,j]*imarray_moyenne_blue[i,j])+(c2_blue*imarray_moyenne_blue[i,j])+d2_blue



# application de la méthode des moindre carré pour déterminer la dose à partir des 3 couleurs

imarray_dose_final = np.zeros((rows, cols))
for x in range(0, rows-1):
    for y in range(0, cols-1):
        list=[]
        list.append(imarray_dose_red[x,y])
        list.append(imarray_dose_green[x,y])
        list.append(imarray_dose_blue[x,y])
        print (list)
        min = np.amin(list)
#        print (min)
        max = np.amax(list)
#        print (max)
        delta_red = min - imarray_dose_red[x,y]
        delta_green = min - imarray_dose_green[x,y]
        delta_blue = min - imarray_dose_blue[x,y]
        min_square_init = np.sqrt((delta_red*delta_red)+(delta_green*delta_green)+(delta_blue*delta_blue))
#        print(min_square_init)
        d = min + 0.01
        while d < max:
            delta_red = d-imarray_dose_red[x,y]
            delta_green = d-imarray_dose_green[x,y]
            delta_blue = d-imarray_dose_blue[x,y]
            min_square = np.sqrt((delta_red*delta_red)+(delta_green*delta_green)+(delta_blue*delta_blue))
#            print (min_square, d)
            if min_square < min_square_init:
                min_square_init = min_square
                d = d + 0.01
            if min_square > min_square_init:
                imarray_dose_final[x,y] = d - 0.01
                break

                
      


            

# sauvegarde de la matrice de dose #############################################

#print (imarray[0,0])
imarray_dose = np.float32(imarray_dose_final)
resolution_mm = 2.54/75

#print (imarray_dose[0,0])
tiff.imshow(imarray_dose_final)
nnetiff.imsave(file[0:len(file)-6] + 'dose_3couleurs.tiff', imarray_dose, resolution=(1/resolution_mm, 1/resolution_mm , 'CENTIMETER'))

