import matplotlib.pyplot as plt

available_trajectories = 20

data_files = []

rho_a = []

for x in range(1, available_trajectories + 1):
    data_files.append("traj" + str(x) + ".out")

for data_file in data_files:
    with open(data_file) as file:

