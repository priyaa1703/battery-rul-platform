from scipy.io import loadmat

mat = loadmat('data/B0005.mat')
data = mat['B0005'][0, 0]
cycles = data['cycle'][0]

for cycle in cycles:
    if cycle['type'][0] == 'impedance':
        print("Found an impedance cycle.")
        measurements = cycle['data'][0, 0]
        print("Fields inside it:", measurements.dtype.names)
        break