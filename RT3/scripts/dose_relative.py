import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    for et in etude:
        plt.figure(figsize=(12, 7))
        df_cc13_10 = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx',  et + ' 10cm')
        # df_cc13_3 = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx',  et + ' 3cm')
        plt.plot(df_cc13_10.iloc[:, 0], df_cc13_10.iloc[:, 1], ':', label='CC13')
        for det in detecteurs:
            df_10 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', et + ' 10x10')
            plt.plot(df_10.iloc[:, 0], df_10.iloc[:, 1], lw=0.75, label= det)
        plt.xlabel(df_10.columns[0] + ' (mm)')
        plt.ylabel('Dose (%)')
        plt.legend(loc='upper right', fontsize=8)
        plt.title(et + r' pour un champ 10x10 cm$^2$')
        plt.grid(ls='--')
        plt.savefig('figures/dose_relative/test/' + et + '.png', dpi=250)

    for champ in ['10x10', '3x3']:
        df_CC13 = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx', 'Crossline ' + champ.split('x')[0] + 'cm')
        plt.figure(figsize=(12, 7))
        plt.plot(df_CC13.iloc[:, 0], df_CC13.iloc[:, 1], lw=0.75, label='CC13')
        for det in detecteurs:
            df_crossline = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', 'Crossline ' + champ)
            df_inline_10 = pd.read_excel('../mesures/export_excel/' + det + '.xlsx', 'Inline ' + champ)
            plt.plot(df_crossline.iloc[:, 0], df_crossline.iloc[:, 1],label=det, lw=0.75)
        plt.xlabel('Distance (mm)')
        plt.ylabel('Dose (%)')
        plt.title('Influence du détecteur')
        plt.legend()
        plt.grid(ls='--')
        plt.savefig('figures/dose_relative/test/profils_' + champ + '.png', dpi=250)

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
    plt.savefig('figures/dose_relative/chambre_ref.png', dpi=250)

def DSP():
    for et in ['Crossline X6 DSP ', 'Rendement X6 DSP ']:
        plt.figure(figsize=(12, 7))
        df_100 = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx', et[:-7] + '10cm')
        for dsp in ['85cm', '110cm']:
            df = pd.read_excel('/Volumes/LEXAR/Fiches_DQ/RT/RT3/mesures/export_excel/6_DSP.xlsx', sheet_name=et + dsp)
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=dsp)
        plt.plot(df_100.iloc[:, 0], df_100.iloc[:, 1], label='100cm')
        plt.grid(ls='--')
        plt.legend()
        plt.xlabel('Profondeur (mm)')
        plt.ylabel('Dose (%)')
        plt.title('Influence de la DSP')
        plt.xlim(0, 25)
        plt.ylim(80, 102)
        plt.savefig('figures/dose_relative/DSP/' + et.split(' ')[0] + '_DSP_zoom.png', dpi=250)

def rendement_X6_X23():
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
    for energie in ['X6', 'X23']:
        df = pd.read_excel('../mesures/export_excel/2_profils_ouverture_fermeture.xlsx', 'Ouverture Crossline ' + energie)
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=energie)
    plt.title('Influence de l\'énergie sur les profils')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose (%)')
    plt.grid(ls='--')
    plt.legend()
    plt.savefig('figures/dose_relative/profils/profils_energie.png', dpi=250)

    plt.figure(figsize=(12, 7))
    for champ in ['3x3', '6x6', '20x20']:
        df = pd.read_excel('../mesures/export_excel/champ_' + champ + '.xlsx', 'Rendement X6')
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=champ + r' cm$^2$')
    df = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx', 'Rendement 10cm')
    plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=r'10x10 cm$^2$')
    plt.grid(ls='--')
    plt.legend()
    plt.title('Influence de la taille de champ')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose (%)')
    plt.savefig('figures/dose_relative/rendement_champs.png', dpi=250)

    plt.figure(figsize=(14, 7))
    for champ in ['3x3', '6x6', '8x8', '12x12', '15x15', '20x20']:
        df = pd.read_excel('../mesures/export_excel/champ_' + champ + '.xlsx', 'Crossline X6 Ouverture')
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label='Champ ' + champ)
    plt.grid(ls='--')
    plt.legend()
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose (%)')
    plt.title('Tailles de champ')
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(15))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(5))
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

def vitesse():
    plt.figure(figsize=(12, 7))
    for vit in ['Continu Lent', 'Continu Rapide', 'SS5']:
        df = pd.read_excel('../mesures/export_excel/1_continu_SS.xlsx', vit)
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=vit)
    plt.grid(ls='--')
    plt.legend()
    plt.show()

def inline_crossline():
    plt.figure(figsize=(12, 7))
    for profil in ['Inline', 'Crossline']:
        df = pd.read_excel('../mesures/export_excel/14_profils_rendements_cc13.xlsx', profil + ' 10cm')
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=profil)
    plt.legend()
    plt.grid(ls='--')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Dose (%)')
    plt.title('Orientation du profil de dose')
    plt.savefig('figures/dose_relative/orientation_profil.png', dpi=250)

def SS():
    # for i in range(7):
    df = pd.ExcelFile('../mesures/export_excel/1_continu_SS.xlsx')
    with df as xlsx:
        plt.subplots(1, 4, figsize=(18, 5))
        for i in range(4):
            df_sheet = pd.read_excel(xlsx, sheet_name=i)
            plt.subplot(1, 4, i+1)
            if i < 2:
                plt.title(df.sheet_names[i])
            else:
                plt.title('Pas ' +  df.sheet_names[i].split('_')[0] + 'mm ' + df.sheet_names[i].split('_')[1] + 'mm ' + df.sheet_names[i].split('_')[2] + 's')
            plt.scatter(df_sheet.iloc[:, 0], df_sheet.iloc[:, 1], marker='x')
            plt.xlabel('Distance (mm)')
            plt.ylabel('Dose (%)')
            plt.grid(ls='--')
        plt.savefig('figures/dose_relative/step_by_step/step_by_step_1.png', dpi=250)
        plt.subplots(1, 3, figsize=(14, 5))
        for i in range(4, 7, 1):
            df_sheet = pd.read_excel(xlsx, sheet_name=i)
            plt.subplot(1, 3, i-3)
            plt.title('Pas ' +  df.sheet_names[i].split('_')[0] + 'mm ' + df.sheet_names[i].split('_')[1] + 'mm ' + df.sheet_names[i].split('_')[2] + 's')
            plt.scatter(df_sheet.iloc[:, 0], df_sheet.iloc[:, 1], marker='x')
            plt.xlabel('Distance (mm)')
            plt.ylabel('Dose (%)')
            plt.grid(ls='--')
        plt.savefig('figures/dose_relative/step_by_step/step_by_step_2.png', dpi=250)

def main():
    # courbes_solo()
    # influence_detecteur()
    # chambre_ref()
    DSP()
    # rendement_X6_X23()
    # champs()
    # perturbations_chambre_ref()
    # vitesse()
    # inline_crossline()
    # SS()

main()