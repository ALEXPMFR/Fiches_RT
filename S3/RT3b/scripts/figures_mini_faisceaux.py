import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_files = list(Path('../queues_mesures/output/export_csv_premiere_session/arrangement_donnees').glob('champ*.csv'))

def extract_energie(file_name):
    energy = file_name.stem.split('_')[-1]
    return energy

def extract_taille_champ(file_name):
    field_width = file_name.stem.split('_')[1]
    return field_width

def figures_profils():
    for csv in csv_files:
        df = pd.read_csv(csv, delimiter=';', decimal=',')
        df = df.dropna(how='all', axis=1)
        df.columns = ['Crossline (mm)', 'Dose Crossline (%)', 'Inline (mm)', 'Dose Inline (%)', 'Depth (mm)', 'Dose Depth (%)']
        plt.figure(figsize=(12, 7))
        plt.plot(df['Crossline (mm)'], df['Dose Crossline (%)'], label='Crossline')
        plt.plot(df['Inline (mm)'], df['Dose Inline (%)'], label=('Inline'))
        plt.title(f'Profils de dose {extract_taille_champ(csv)} {extract_energie(csv)}')
        plt.xlabel('Distance (mm)')
        plt.ylabel('Dose (%)')
        plt.grid(ls='--')
        plt.legend()
        plt.savefig(f'output/profils/{csv.stem}.png', dpi=250)

def figures_rendements_6FFF():
    plt.figure(figsize=(12, 7))
    for csv in csv_files:
        df = pd.read_csv(csv, delimiter=';', decimal=',')
        df = df.dropna(how='all', axis=1)
        df.columns = ['Crossline (mm)', 'Dose Crossline (%)', 'Inline (mm)', 'Dose Inline (%)', 'Depth (mm)', 'Dose Depth (%)']
        df['Dose Depth (%)'] = df['Dose Depth (%)'] / df['Dose Depth (%)'].max() * 100
        if extract_energie(csv) == '6FFF':
            plt.plot(df['Depth (mm)'], df['Dose Depth (%)'], lw=1, label=extract_taille_champ(csv))
            plt.grid(ls='--')
            plt.xlabel('Profondeur (mm)')
            plt.ylabel('Dose (%)')
            plt.legend()
            plt.title('Rendements en profondeur pour différentes tailles de champs')
    plt.show()

def main():
    figures_profils()
    # figures_rendements_6FFF()

main()