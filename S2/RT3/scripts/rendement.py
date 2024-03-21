import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('../mesures/RT3_absolue.xlsx', 'RDT fin')[:24]
df['Dose X6 (%)'] = df['Charge X6 (nC)'] / df['Charge X6 (nC)'].max() * 100
df['Dose X23 (%)'] = df['Charge X23 (nC)'] / df['Charge X23 (nC)'].max() * 100

rdt20_10_X6 = df['Charge X6 (nC)'][20]/df['Charge X6 (nC)'][10]
rdt20_10_X23 = df['Charge X23 (nC)'][20]/df['Charge X23 (nC)'][10]
IQ_X6 = 1.2661 * rdt20_10_X6 - 0.0595
IQ_X23 = 1.2661 * rdt20_10_X23 - 0.0595
D20_D10_X23 = df['Charge X23 (nC)'][20] / df['Charge X23 (nC)'][10]
D20_D10_X6 = df['Charge X6 (nC)'][20] / df['Charge X6 (nC)'][10]

# plt.figure(figsize=(10, 5))
# plt.scatter(df['Profondeur (cm)'], df['Dose X6 (%)'], marker='x', label='X6')
# plt.scatter(df['Profondeur (cm)'], df['Dose X23 (%)'], marker='x', label='X23')
# plt.legend()
# plt.grid(ls='--')
# plt.title('Rendement en profondeur (Clinac 2)')
# plt.xlabel('Profondeur (cm)')
# plt.ylabel('Dose relative (%)')
# plt.ylim(0, 1.1)
# # plt.savefig('figures/rdt.png', dpi=300)
# plt.show()

zmax_X6 = df.loc[df['Charge X6 (nC)'] == df['Charge X6 (nC)'].max()]['Profondeur (cm)'].mean()
zmax_X23 = df.loc[df['Charge X23 (nC)'] == df['Charge X23 (nC)'].max()]['Profondeur (cm)'].mean()

df['RTM X6'] = df['Dose X6 (%)'] * ((100 + df['Profondeur (cm)']) / (100 + zmax_X6))**2
df['RTM X23'] = df['Dose X23 (%)'] * ((100 + df['Profondeur (cm)']) / (100 + zmax_X23))**2
df['RTM X6 norm (%)'] = df['RTM X6'] / df['RTM X6'].max() * 100
df['RTM X23 norm (%)'] = df['RTM X23'] / df['RTM X23'].max() * 100

# plt.scatter(df['Profondeur (cm)'], df['RTM X6'], label='RTM')
# plt.scatter(df['Profondeur (cm)'], df['Dose X6 (%)'], label='RDT')
# plt.legend()
# plt.show()
print(df)

energie = ['6', '23']
plt.subplots(2, 1, figsize=(14, 8))
for ene in range(len(energie)):
    plt.subplot(2, 1, ene+1)
    plt.plot(df['Profondeur (cm)'], df['Dose X' + energie[ene] + ' (%)'], label='RDT')
    plt.plot(df['Profondeur (cm)'], df['RTM X' + energie[ene] + ' norm (%)'], label='RTM')
    plt.legend()
    plt.title('RDT et RTM X' + energie[ene] + ' Clinac 2')
    plt.xlabel('Profondeur (cm)')
    plt.ylabel('Dose relative (%)')
    plt.grid(ls='--')
    plt.ylim(0, 104)
# plt.savefig('figures/comp_RDT_RTM.png', dpi=300)
plt.show()