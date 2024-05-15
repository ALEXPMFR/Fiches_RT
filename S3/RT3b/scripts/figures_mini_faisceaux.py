import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from modules_figures import extract_energie, extract_taille_champ, creation_dataframe

csv_files = list(Path('../queues_mesures/output/export_csv_premiere_session/arrangement_donnees').glob('champ*.csv'))

def figures_profils(orientation):
    for csv in csv_files:
        df = creation_dataframe(csv)
        plt.figure(figsize=(12, 7))
        plt.plot(df[f'{orientation} (mm)'], df[f'Dose {orientation} (%)'], label=orientation)
        plt.title(f'Profils de dose {extract_taille_champ(csv)} {extract_energie(csv)}')
        plt.xlabel('Distance (mm)')
        plt.ylabel('Dose (%)')
        plt.grid(ls='--')
        plt.legend()
        plt.savefig(f'output/profils/{csv.stem}.png', dpi=250)

def figures_rendements_6FFF():
    plt.figure(figsize=(12, 7))
    for csv in csv_files:
        df = creation_dataframe(csv)
        if extract_energie(csv) == '6FFF':
            plt.plot(df['Depth (mm)'], df['Dose Depth (%)'], lw=1, label=extract_taille_champ(csv))
            plt.grid(ls='--')
            plt.xlabel('Profondeur (mm)')
            plt.ylabel('Dose (%)')
            plt.legend()
            plt.title('Rendements en profondeur pour différentes tailles de champs')
            plt.xlim(0, 250)
            plt.ylim(0, 102)
    plt.savefig('output/rendements/comp_tailles_champ.png', dpi=250)

def comp_rdt_energie():
    plt.figure(figsize=(12, 7))
    for csv in csv_files[:2]:
        df = creation_dataframe(csv)
        plt.plot(df['Depth (mm)'], df['Dose Depth (%)'], label=extract_energie(csv))
    plt.xlim(0, 250)
    plt.ylim(0, 102)
    plt.xlabel('Profondeur (mm)')
    plt.ylabel('Dose (%)')
    plt.grid(ls='--')
    plt.legend()
    plt.savefig('output/rendements/comp_rdt_6FFF_6MV.png', dpi=250)

def comp_profils_energie(orientation):
    plt.figure(figsize=(12, 7))
    for csv in csv_files[:2]:
        df = creation_dataframe(csv)
        plt.plot(df[f'{orientation} (mm)'], df[f'Dose {orientation} (%)'], label=extract_energie(csv))
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose (%)')
    plt.grid(ls='--')
    plt.legend()
    plt.title(f'Profils de dose en fonction de l\'énergie pour un champ de 1 cm x 1 cm {orientation}')
    plt.savefig(f'output/profils/energie/comp_profils_{orientation}_energie.png', dpi=250)

def comp_profils_tailles_champs(orientation):
    for csv in csv_files:
        if extract_energie(csv) == '6FFF':
            df = creation_dataframe(csv)
            field_width = extract_taille_champ(csv)
            plt.plot(df[f'{orientation} (mm)'], df[f'Dose {orientation} (%)'], label=field_width + ' ' + orientation)
            plt.legend(fontsize=8)
            plt.grid(ls='--')
            plt.xlabel('Distance (mm)')
            plt.ylabel('Dose (%)')
            plt.title('Profils de dose en fonction de la taille de champ et de l\'orientation')

def main():
    # figures_profils('Inline')
    # figures_profils('Crossline')
    # figures_rendements_6FFF()
    # comp_rdt_energie()
    # comp_profils_energie('Inline')
    # comp_profils_energie('Crossline')
    plt.figure(figsize=(12, 7))
    comp_profils_tailles_champs('Inline')
    comp_profils_tailles_champs('Crossline')
    plt.show()

main()