from scipy.io import loadmat
import pandas as pd
import matplotlib.pyplot as plt



def extract_capacity_fade(battery_name):
    mat = loadmat(f'data/{battery_name}.mat')
    data = mat[battery_name][0, 0]
    cycles = data['cycle'][0]
    print(mat.keys())
    print(data.dtype.names)

    capacities = []
    cycle_numbers = []
    discharge_count = 0

    for cycle in cycles:
        if cycle['type'][0] == 'discharge':
            discharge_count += 1
            capacity = cycle['data'][0, 0]['Capacity'][0][0]
            capacities.append(capacity)
            cycle_numbers.append(discharge_count)

    df = pd.DataFrame({
        'discharge_cycle_number': cycle_numbers,
        'capacity_ah': capacities
    })
    return df

# Run this for all 4 batteries
battery_names = ['B0005', 'B0006', 'B0007', 'B0018']

plt.figure(figsize=(10, 6))

for name in battery_names:
    df = extract_capacity_fade(name)
    df.to_csv(f'data/{name}_capacity_fade.csv', index=False)
    print(f"{name}: {len(df)} discharge cycles, starting capacity {df['capacity_ah'].iloc[0]:.3f}Ah, ending capacity {df['capacity_ah'].iloc[-1]:.3f}Ah")
    plt.plot(df['discharge_cycle_number'], df['capacity_ah'], label=name)

plt.axhline(y=1.4, color='red', linestyle='--', label='End-of-Life threshold (1.4Ah)')
plt.xlabel('Discharge Cycle Number')
plt.ylabel('Capacity (Ah)')
plt.title('Battery Capacity Fade Over Time (Real NASA Data)')
plt.legend()
plt.grid(True)
plt.savefig('data/capacity_fade_plot.png')
plt.show()
