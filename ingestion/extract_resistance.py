from scipy.io import loadmat
import pandas as pd
import matplotlib.pyplot as plt

def extract_resistance_trend(battery_name):
    mat = loadmat(f'data/{battery_name}.mat')
    data = mat[battery_name][0, 0]
    cycles = data['cycle'][0]

    re_values = []
    rct_values = []
    impedance_cycle_number = []
    count = 0

    for cycle in cycles:
        if cycle['type'][0] == 'impedance':
            count += 1
            measurements = cycle['data'][0, 0]
            re = measurements['Re'][0][0]
            rct = measurements['Rct'][0][0]
            re_values.append(re)
            rct_values.append(rct)
            impedance_cycle_number.append(count)

    df = pd.DataFrame({
        'impedance_cycle_number': impedance_cycle_number,
        'Re': re_values,
        'Rct': rct_values
    })
    return df

battery_names = ['B0005', 'B0006', 'B0007', 'B0018']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for name in battery_names:
    df = extract_resistance_trend(name)
    df.to_csv(f'data/{name}_resistance.csv', index=False)
    print(f"{name}: {len(df)} impedance measurements taken")
    axes[0].plot(df['impedance_cycle_number'], df['Re'], label=name)
    axes[1].plot(df['impedance_cycle_number'], df['Rct'], label=name)

axes[0].set_title('Electrolyte Resistance (Re) Over Time')
axes[0].set_xlabel('Impedance Measurement Number')
axes[0].set_ylabel('Re (Ohms)')
axes[0].legend()
axes[0].grid(True)

axes[1].set_title('Charge Transfer Resistance (Rct) Over Time')
axes[1].set_xlabel('Impedance Measurement Number')
axes[1].set_ylabel('Rct (Ohms)')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('data/resistance_trend_plot.png')
plt.show()