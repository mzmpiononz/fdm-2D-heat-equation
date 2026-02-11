import os
from dotenv import load_dotenv
from wall_2d_fdm import Wall2dFDM

# Load .env file
load_dotenv()

# load variables
length = float(os.getenv('LENGTH'))
larger = float(os.getenv('LARGER'))
lambd = float(os.getenv('LAMBD'))
delta_xy = float(os.getenv('DELTA_XY'))
t_ext = int(os.getenv('T_EXT'))
t_int = int(os.getenv('T_INT'))
h_ext = int(os.getenv('H_EXT'))
h_int = int(os.getenv('H_INT'))
u_initial = int(os.getenv('U_INITIAL'))
max_iter_time = int(os.getenv('MAX_ITER_TIME'))

# instatiate the method
job = Wall2dFDM(
        length=length, larger=larger, lambd=lambd,
        delta_xy=delta_xy, t_ext=t_ext, t_int=t_int,
        h_ext=h_ext, h_int=h_int, u_initial=u_initial,
        max_iter_time=max_iter_time
)

# plot the mesh grid
job.plot_grid_nodes()
# run the simulation
u = job.calculate_temperatures()
t = u[-1]
# plot the heat map
print('plotting heat map')
job.plot_heat_map(t)
# calculate the heat flow
q = round(job.calculate_heat_flow(t), 2)
print(f'heat flow : {q} W')