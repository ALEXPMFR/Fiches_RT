import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

excel_files = list(Path('../export_excel/').rglob('*.xlsx'))

def unique():
    for fic in excel_files:
        df = pd.ExcelFile(str(fic))
        for sheet in df.sheet_names:
            df = pd.read_excel(str(fic), sheet)

            orientation = sheet.split('_')[0]
            energie = str(int(sheet.split('_')[1][:2]))
            taille_champ = sheet.split('_')[2] + 'x' + sheet.split('_')[2] + r' cm$^2$'
            dsp = sheet.split('_')[3][3:] + ' cm'

            if orientation == 'cr':
                orientation = 'Crossline'
            elif orientation == 'in':
                orientation = 'Inline'

            plt.figure(figsize=(12, 7))
            plt.plot(df.iloc[:, 0], df.iloc[:, 1])
            plt.xlabel('Distance (mm)')
            plt.ylabel('Dose relative (%)')
            plt.grid(ls='--')
            plt.title(orientation + ' ' + energie + ' MeV ' + taille_champ + ' ' + dsp)
            plt.show()

def rendements_energies():
    df = pd.ExcelFile('../export_excel/rendements.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        if sheet.split('_')[2] == '10' and sheet.split('_')[3] == 'DSP100' and sheet.split('_')[4] == 'ROOS':
            orientation = sheet.split('_')[0]
            energie = str(int(sheet.split('_')[1][:2]))
            taille_champ = sheet.split('_')[2] + 'x' + sheet.split('_')[2] + r' cm$^2$'
            dsp = sheet.split('_')[3][3:] + ' cm'
            if orientation == 'cr':
                orientation = 'Crossline'
            elif orientation == 'in':
                orientation = 'Inline'
            df = pd.read_excel('../export_excel/rendements.xlsx', sheet)
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=energie + ' MeV')
            plt.grid(ls='--')
            plt.title('Rendement en profondeur en fonction del\'énergie')
            plt.xlabel('Profondeur (mm)')
            plt.ylabel('Dose relative (%)')
            plt.xlim(0, 110)
            plt.ylim(0, 102)
            plt.legend()
    plt.savefig('figures/rendements_energies.png', dpi=250)

def rendements_DSP():
    df = pd.ExcelFile('../export_excel/rendements.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        if sheet.split('_')[2] == '10' and sheet.split('_')[1] == '09MeV' and sheet.split('_')[4] == 'ROOS':
            # orientation = sheet.split('_')[0]
            # energie = str(int(sheet.split('_')[1][:2]))
            # taille_champ = sheet.split('_')[2] + 'x' + sheet.split('_')[2] + r' cm$^2$'
            # dsp = sheet.split('_')[3][3:] + ' cm'
            # if orientation == 'cr':
            #     orientation = 'Crossline'
            # elif orientation == 'in':
            #     orientation = 'Inline'
            df = pd.read_excel('../export_excel/rendements.xlsx', sheet)
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=sheet.split('_')[3][3:])
    plt.grid(ls='--')
    plt.xlabel('Profondeur (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Rendement en profondeur en fonction de la DSP')
    plt.legend()
    plt.xlim(0, 60)
    plt.ylim(0, 102)
    plt.savefig('figures/rendements_DSP.png', dpi=250)

def rendements_champs():
    df = pd.ExcelFile('../export_excel/rendements.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in sorted(df.sheet_names):
        df = pd.read_excel('../export_excel/rendements.xlsx', sheet)
        if sheet.split('_')[1] == '09MeV' and sheet.split('_')[3] == 'DSP100' and sheet.split('_')[4] == 'CC13':
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], lw=1, label=sheet.split('_')[2] + r' cm$^2$')
    plt.xlim(0, 75)
    plt.ylim(0, 102)
    plt.grid(ls='--')
    plt.xlabel('Profondeur (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Rendement en profondeur en fonction de la taille de champ')
    plt.legend()
    plt.savefig('figures/rendements_taille_champ.png', dpi=250)

def rendements_detecteurs():
    df = pd.ExcelFile('../export_excel/rendements.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        df = pd.read_excel('../export_excel/rendements.xlsx', sheet)
        if sheet.split('_')[1] == '09MeV' and sheet.split('_')[2] == '10' and sheet.split('_')[3] == 'DSP100':
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=sheet.split('_')[-1])
    plt.xlabel('Profondeur (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Rendement en profondeur en fonction du détecteur')
    plt.legend()
    plt.grid(ls='--')
    plt.savefig('figures/rendements_detecteurs.png', dpi=250)
    plt.xlim(0, 75)
    plt.ylim(0, 102)

def profils_energies():
    df = pd.ExcelFile('../export_excel/profils.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        df = pd.read_excel('../export_excel/profils.xlsx', sheet)
        if sheet.split('_')[0] == 'CR' and sheet.split('_')[2] == '10' and sheet.split('_')[3] == 'DSP100' and sheet.split('_')[4] == 'CC13' and len(sheet.split('_')) == 5:
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], lw=1, label=str(int(sheet.split('_')[1][:2])) + ' MeV')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Profil de dose en fonction de l\'énergie')
    plt.legend()
    plt.grid(ls='--')
    plt.xlim(-100, 100)
    plt.savefig('figures/profils_energies.png', dpi=250)

def profils_DSP():
    df = pd.ExcelFile('../export_excel/profils.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        df = pd.read_excel('../export_excel/profils.xlsx', sheet)
        if sheet.split('_')[0] == 'CR' and sheet.split('_')[1] == '09MeV' and sheet.split('_')[2] == '10' and sheet.split('_')[4] == 'CC13' and len(sheet.split('_')) == 5:
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label= 'DSP ' + sheet.split('_')[3][3:] + ' cm')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Profil de dose en fonction de la DSP')
    plt.grid(ls='--')
    plt.xlim(-100, 100)
    plt.legend()
    plt.savefig('figures/profils_DSP.png', dpi=250)

def profils_detecteurs():
    df = pd.ExcelFile('../export_excel/profils.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        df = pd.read_excel('../export_excel/profils.xlsx', sheet)
        if sheet.split('_')[0] == 'CR' and sheet.split('_')[1] == '09MeV' and sheet.split('_')[2] == '10' and sheet.split('_')[3] == 'DSP100' and len(sheet.split('_')) == 5:
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=sheet.split('_')[-1])
    plt.grid(ls='--')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Profil de dose en fonction du détecteur')
    plt.legend()
    plt.show()

def profils_orientation():
    df = pd.ExcelFile('../export_excel/profils.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        df = pd.read_excel('../export_excel/profils.xlsx', sheet)
        if sheet.split('_')[1] == '09MeV' and sheet.split('_')[2] == '10' and sheet.split('_')[3] == 'DSP100' and sheet.split('_')[4] == 'CC13' and len(sheet.split('_')) == 5:
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=df.columns[0])
    plt.grid(ls='--')
    plt.legend()
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Profil de dose en fonction de l\'orientation')
    plt.xlim(-100, 100)
    plt.savefig('figures/profils_orientation.png', dpi=250)

def profils_vitesse():
    df = pd.ExcelFile('../export_excel/profils.xlsx')
    plt.figure(figsize=(12, 7))
    for sheet in df.sheet_names:
        df = pd.read_excel('../export_excel/profils.xlsx', sheet)
        if len(sheet.split('_')) == 6:
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=sheet.split('_')[-1])
    plt.legend()
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose relative (%)')
    plt.title('Profil de dose en fonction de la vitesse d\'acquisition')
    plt.xlim(-100, 100)
    plt.grid(ls='--')
    plt.show()

def main():
    unique()
    rendements_energies()
    rendements_DSP()
    rendements_champs()
    rendements_detecteurs()
    profils_energies()
    profils_DSP()
    profils_detecteurs()
    profils_orientation()
    profils_vitesse()

main()