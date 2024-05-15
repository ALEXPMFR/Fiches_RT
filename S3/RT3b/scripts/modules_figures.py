import pandas as pd

def extract_energie(file_name):
    energy = file_name.stem.split('_')[-1]
    return energy

def extract_taille_champ(file_name):
    field_width = file_name.stem.split('_')[1]
    return field_width

def creation_dataframe(file_name):
    df = pd.read_csv(file_name, delimiter=';', decimal=',')
    df = df.dropna(how='all', axis=1)
    df.columns = ['Crossline (mm)', 'Dose Crossline (%)', 'Inline (mm)', 'Dose Inline (%)', 'Depth (mm)', 'Dose Depth (%)']
    df.columns = ['Crossline (mm)', 'Dose Crossline (%)', 'Inline (mm)', 'Dose Inline (%)', 'Depth (mm)', 'Dose Depth (%)']
    df['Dose Depth (%)'] = df['Dose Depth (%)'] / df['Dose Depth (%)'].max() * 100
    return df