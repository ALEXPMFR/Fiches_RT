import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_excel('../mesures/foc.xlsx')
df = df.dropna()
df.columns = ['Champ (cm2)', 'Charge (nC)', 'Charge moyenne (nC)', 'FOC ref (%)', 'FOC X23 (%)', 'FOC Farmer (%)', 'FOC DSP 80 (%)', 'FOC DSP 120 (%)']

plt.figure(figsize=(12, 7))
plt.scatter(df['Champ (cm2)'], df['FOC ref (%)'], marker='x', label='CC13 X6')
plt.scatter(df['Champ (cm2)'], df['FOC X23 (%)'], marker='x', label='CC13 X23')
plt.scatter(df['Champ (cm2)'], df['FOC Farmer (%)'], marker='x', label='Farmer X6')
plt.scatter(df['Champ (cm2)'], df['FOC DSP 80 (%)'], marker='x', label='CC13 DSP 80 cm')
plt.scatter(df['Champ (cm2)'], df['FOC DSP 120 (%)'], marker='x', label='CC13 DSP 120 cm')
plt.grid(ls='--')
plt.legend()
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1))
plt.xlim(0, 21)
plt.xlabel('Tailles de champ (cm)')
plt.ylabel('Dose (%)')
plt.title('FOC')
# plt.xlim(0, 21)
plt.savefig('figures/dose_relative/FOC.png', dpi=250)