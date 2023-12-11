import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('/Users/alexandrerintaud/Desktop/matrices.xlsx')

mean_dose = []
for ene in [6, 23]:
    for champ in df.loc[df['Energie'] == 6, :]['Champs'][::3]:
        mean_dose.append(df.loc[df['Energie'] == ene, :].loc[df['Champs'] == champ]['Dose'].mean())

df = df[::3]
df['Dose'] = mean_dose

plt.figure(figsize=(12, 7))
for ene in [6, 23]:
    champ_10 = float(df.loc[df['Energie'] == ene, :].loc[df['Champs'] == 10, 'Dose'])
    plt.scatter(df.loc[df['Energie'] == ene, :]['Champs'], df.loc[df['Energie'] == ene, :]['Dose'] / champ_10, label=str(ene) + ' MV')
    plt.legend()
    plt.title('FOC avec matrice PTW 1500')
    plt.xlabel('Taille de champ carré (cm)')
    plt.ylabel('Dose (%)')
    plt.grid(ls='--')
plt.savefig('/Volumes/LEXAR/Fiches_DQ/RT/RT5/scripts/figures/FOC_1500.png', dpi=250)