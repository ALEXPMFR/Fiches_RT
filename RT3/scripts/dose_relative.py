import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

excel_files = sorted(list(Path('../mesures/export_excel/').glob('*.xlsx')))

def courbes_solo():
    for fic in excel_files:
        df = pd.read_excel(str(fic), decimal=',', sheet_name=None)
        for sheet in range(len(df)):
            df = pd.read_excel(str(fic), sheet_name=sheet)
            print(df)
            plt.figure(figsize=(12, 7))
            plt.plot(df.iloc[:, 0], df.iloc[:, 1])
            plt.title(str(fic.stem) + ' ' + str(sheet))
            plt.xlabel(df.columns[0] + ' (mm)')
            plt.ylabel('Dose (%)')
            plt.grid(ls='--')
            plt.show()

def influence_detecteur():
    detecteurs = ['diode', 'microdiamant', 'semiflex', 'pinpoint']
    etude = ['Rendement', 'Inline', 'Crossline']
    for det in detecteurs:
        for et in etude:
            df_10 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', et + ' 10x10')
            df_3 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', et + ' 3x3')
            df_cc13_10 = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx',  et + ' 10cm')
            df_cc13_3 = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx',  et + ' 3cm')
            plt.figure(figsize=(12, 7))
            plt.plot(df_10.iloc[:, 0], df_10.iloc[:, 1], label= det + ' 10x10 cm2')
            plt.plot(df_3.iloc[:, 0], df_3.iloc[:, 1], label= det + ' 3x3 cm2')
            plt.plot(df_cc13_10.iloc[:, 0], df_cc13_10.iloc[:, 1], ':', label='CC13 10x10 cm2')
            plt.plot(df_cc13_3.iloc[:, 0], df_cc13_3.iloc[:, 1], ':', label='CC13 3x3 cm2')
            plt.xlabel(df_10.columns[0] + ' (mm)')
            plt.ylabel('Dose (%)')
            plt.legend(loc='upper right', fontsize=8)
            plt.title(det)
            plt.grid(ls='--')
            plt.savefig('figures/dose_relative/detecteurs/' + det + '_' + et + '.png', dpi=250)

        df_crossline_10 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', 'Crossline 10x10')
        df_inline_10 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', 'Inline 10x10')
        df_crossline_3 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', 'Crossline 3x3')
        df_inline_3 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', 'Inline 3x3')
        plt.figure(figsize=(12, 7))
        plt.plot(df_crossline_10.iloc[:, 0], df_crossline_10.iloc[:, 1], label='Crossline 10x10 cm2')
        plt.plot(df_inline_10.iloc[:, 0], df_inline_10.iloc[:, 1], label='Inline 10x10 cm2')
        plt.plot(df_crossline_3.iloc[:, 0], df_crossline_3.iloc[:, 1], label='Crossline 3x3 cm2')
        plt.plot(df_inline_3.iloc[:, 0], df_inline_3.iloc[:, 1], label='Inline 3x3 cm2')
        plt.grid(ls='--')
        plt.legend(loc='upper right', fontsize=8)
        plt.xlabel('Distance (mm)')
        plt.ylabel('Dose (%)')
        plt.title('Profils Inline Crossline ' + det)
        plt.savefig('figures/dose_relative/profils/profils_' + det + '.png', dpi=250)

def chambre_ref():
    plt.figure(figsize=(12, 7))
    for sheet in range(2):
        df = pd.read_excel('../mesures/export_excel/3_sans_chambre_ref.xlsx', sheet_name=sheet)
        plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.title('Influence de la chambre de référence')
    plt.xlabel('Profondeur (mm)')
    plt.ylabel('Dose (%)')
    plt.legend(['Avec référence', 'Sans référence'])
    plt.grid(ls='--')
    plt.savefig('figures/chambre_ref.png', dpi=250)

def DSP():
    for et in ['Crossline X6 DSP ', 'Rendement X6 DSP ']:
        plt.figure(figsize=(12, 7))
        for dsp in ['85cm', '110cm']:
            df = pd.read_excel('/Volumes/LEXAR/Fiches_DQ/RT/RT3/mesures/export_excel/6_DSP.xlsx', sheet_name=et + dsp)
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=dsp)
        plt.grid(ls='--')
        plt.legend()
        plt.xlabel(df.columns[0])
        plt.ylabel('Dose (%)')
        plt.title('Influence de la DSP')
        plt.savefig('figures/dose_relative/DSP/' + et.split(' ')[0] + '_DSP_' + dsp + '.png', dpi=250)

def rendement_X6_X23():
    # plt.figure(figsize=(12, 7))
    # for x in ['14_profils_rendements_cc13.xlsx', '5_X23_RP.xlsx']:
    #     df = pd.read_excel('../mesures/export_excel/' + x, sheet_name=2)
    #     plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    # plt.grid(ls='--')
    # plt.legend(['X6', 'X23'])
    # plt.xlabel('Profondeur (mm)')
    # plt.ylabel('Dose (%)')
    # plt.title('Influence de l\'énergie sur le rendement en profondeur')
    # plt.savefig('figures/dose_relative/rdt_X6_X23.png', dpi=250)

    for energie in ['14_profils_rendements_cc13.xlsx', '5_X23_RP.xlsx']:
        plt.figure(figsize=(12, 7))
        df = pd.read_excel('../mesures/export_excel/' + energie, sheet_name=2)
        df['RTM'] = df.iloc[:, 1] * ((1000 + df.iloc[:, 0]) / (1000 + df.iloc[df.iloc[:, 1].to_list().index(df.iloc[:, 1].max()), 0]))**2
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label='RDT')
        plt.plot(df.iloc[:, 0], df['RTM'], label='RTM')
        plt.legend()
        plt.grid(ls='--')
        plt.xlabel('Profondeur (mm)')
        plt.ylabel('Dose (%)')
        plt.title('RTM et RDT')
        plt.savefig('figures/dose_relative/RTM/' + energie.split('.')[0] + '.png', dpi=250)
        # plt.plot(df.iloc[:, 0], df['RTM'], label='RTM')
        # plt.plot(df.iloc[:, 0], df.iloc[:, 1], label='RDT')
        # plt.show()

def champs():
    for champ in ['3x3', '6x6', '8x8', '12x12', '15x15', '20x20']:
        plt.figure(figsize=(12, 7))
        df_CO = pd.read_excel('../mesures/export_excel/champ_' + champ + '.xlsx', 'Crossline X6 Ouverture')
        df_CF = pd.read_excel('../mesures/export_excel/champ_' + champ + '.xlsx', 'Crossline X6 Fermeture')
        plt.plot(df_CO.iloc[:, 0], df_CO.iloc[:, 1], label='Crossline Ouverture')
        plt.plot(df_CF.iloc[:, 0], df_CF.iloc[:, 1], label='Crossline Fermeture')
        plt.grid(ls='--')
        plt.legend(loc='upper right', fontsize=8)
        plt.xlabel('Distance (mm)')
        plt.ylabel('Dose (%)')
        plt.title('Profils ' + champ + ' cm2')
        plt.savefig('figures/dose_Relative/profils_ouv_fer/profils_' + champ + '.png', dpi=250)

    plt.figure(figsize=(12, 7))
    for champ in ['3x3', '6x6', '8x8', '12x12', '15x15', '20x20']:
        df = pd.read_excel('../mesures/export_excel/champ_' + champ + '.xlsx', 'Crossline X6 Ouverture')
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label='Champ ' + champ)
    plt.grid(ls='--')
    plt.legend()
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose (%)')
    plt.title('Tailles de champ')
    plt.savefig('figures/dose_relative/profils_champs/comp_champs.png', dpi=250)

def perturbations_chambre_ref():
    for energie in ['X6', 'X23']:
        plt.figure(figsize=(12, 7))
        df_norm = pd.read_excel('../mesures/export_excel/2_profils_ouverture_fermeture.xlsx', 'Ouverture Crossline ' + energie)
        df_perturb = pd.read_excel('../mesures/export_excel/13_perturbations_chambre_ref.xlsx', 'Crossline ' + energie)
        plt.plot(df_norm.iloc[:, 0], df_norm.iloc[:, 1], label='Chambre au bord')
        plt.plot(df_perturb.iloc[:, 0], df_perturb.iloc[:, 1], label='Chambre au centre')
        plt.grid(ls='--')
        plt.legend()
        plt.title('Perturbation chambre de référence ' + energie)
        plt.xlabel('Distance (mm)')
        plt.ylabel('Dose (%)')
        plt.savefig('figures/dose_relative/perturbations_chambre/perturbations_' + energie + '.png', dpi=250)



def main():
    # courbes_solo()
    # influence_detecteur()
    # chambre_ref()
    # DSP()
    # rendement_X6_X23()
    champs()
    # perturbations_chambre_ref()


main()