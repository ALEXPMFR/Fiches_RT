champ = [3, 6, 8, 10, 12, 15, 20]
demi_champ = [f/2 for f in champ]
dsp = [80, 120]
profondeur = 10

for d in dsp:
    for c in demi_champ: 
        champ_det = c * 100 / (d + profondeur) * 2 # cm
        print('DSP ', d, '\t Champ iso ', c * 2, '\t Champ deteteur ', round(champ_det, 1))