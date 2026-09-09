import pandas as pd
import numpy as np

def build_combined_dataset(battery_name):
    capacity_df = pd.read_csv(f'data/{battery_name}_capacity_fade.csv')
    resistance_df = pd.read_csv(f'data/{battery_name}_resistance.csv')

    # Resistance was measured on a different, sparser schedule than capacity.
    # We stretch resistance's cycle numbers onto capacity's timeline (0 to 1 scale),
    # so every discharge cycle gets a sensible Re/Rct value even if it wasn't
    # measured at that exact moment.
    capacity_df['progress'] = capacity_df['discharge_cycle_number'] / capacity_df['discharge_cycle_number'].max()
    resistance_df['progress'] = resistance_df['impedance_cycle_number'] / resistance_df['impedance_cycle_number'].max()

    merged = pd.merge_asof(
        capacity_df.sort_values('progress'),
        resistance_df.sort_values('progress'),
        on='progress',
        direction='nearest'
    )

    merged['battery'] = battery_name
    return merged[['battery', 'discharge_cycle_number', 'capacity_ah', 'Re', 'Rct']]

battery_names = ['B0005', 'B0006', 'B0007', 'B0018']
all_data = []

for name in battery_names:
    df = build_combined_dataset(name)
    df.to_csv(f'data/{name}_combined.csv', index=False)
    print(f"{name}: {len(df)} rows, capacity range {df['capacity_ah'].min():.3f}-{df['capacity_ah'].max():.3f}Ah")
    all_data.append(df)

print("\nSample of combined data:")
print(all_data[0].head(10))


def make_sequences(df, window_size=10):
    """Turn a battery's life into overlapping windows of (past readings -> next capacity)."""
    features = df[['capacity_ah', 'Re', 'Rct']].values
    X, y = [], []
    for i in range(len(features) - window_size):
        X.append(features[i:i + window_size])
        y.append(features[i + window_size][0])  # next capacity value
    return np.array(X), np.array(y)


# Build train set from B0005, B0006, B0007 — test set from B0018 (fully unseen battery)
train_names = ['B0005', 'B0006', 'B0007']
test_name = 'B0018'

X_train_list, y_train_list = [], []
for name in train_names:
    df = pd.read_csv(f'data/{name}_combined.csv')
    X, y = make_sequences(df)
    X_train_list.append(X)
    y_train_list.append(y)

X_train = np.concatenate(X_train_list)
y_train = np.concatenate(y_train_list)

df_test = pd.read_csv(f'data/{test_name}_combined.csv')
X_test, y_test = make_sequences(df_test)

print(f"\nTraining sequences: {X_train.shape} -> predicting {y_train.shape}")
print(f"Testing sequences: {X_test.shape} -> predicting {y_test.shape}")

np.save('data/X_train.npy', X_train)
np.save('data/y_train.npy', y_train)
np.save('data/X_test.npy', X_test)
np.save('data/y_test.npy', y_test)
print("\nSaved training/testing arrays to data/ folder.")