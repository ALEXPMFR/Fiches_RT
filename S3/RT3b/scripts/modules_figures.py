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
    df['Dose Depth (%)'] = df['Dose Depth (%)'] / df['Dose Depth (%)'].max() * 100
    return df

def creation_dataframe_mode_acquisition(file_name):
    df = pd.read_csv(file_name, delimiter=';', decimal=',')
    df = df.dropna(how='all', axis=1)

    df.columns = ['Crossline 1_0,5 (mm)', 'Dose 1_0,5 (%)', 'Crossline 2_0,01 (mm)', 'Dose 2_0,01 (%)', 'Crossline 0,1_0,01 (mm)', 'Dose 0,1_0,01 (%)', 'Crossline continu_2,5 (mm)', 'Dose continu_2,5 (%)', 'Crossline continu_1 (mm)', 'Dose continu_1 (%)', 'Crossline continu_0,3 (mm)', 'Dose continu_0,3 (%)', 'Crossline continu_0,5 (mm)', 'Dose continu_0,5 (%)']
    return df

# def extract_pas_integration(file_name):
    