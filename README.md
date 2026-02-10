# fdm-2D-heat-equation
Finite Difference Method with python applied on 2D heat equation

## APPLICATION : calculation of a heat flow through a part of a wall

install requirements
```
pip install requirements.txt
```

run the method

```python
import os
from dotenv import load_dotenv
from wall_2d_fdm import Wall2dFDM

# Load .env file
load_dotenv()

# load variables
# length of the wall (horizontal) (m)
length = float(os.getenv('LENGTH'))
# larger of the wall (vertical) (m)
larger = float(os.getenv('LARGER'))
# thermal conductivity of the wall (W/m.K)
lambd = float(os.getenv('LAMBD'))
# delta_xy : mesh steps (m)
delta_xy = float(os.getenv('DELTA_XY'))
# outside temperature (°C)
t_ext = int(os.getenv('T_EXT'))
# inside temperature (°C)
t_int = int(os.getenv('T_INT'))
# outside thermal convection coefficient (W/m².K)
h_ext = int(os.getenv('H_EXT'))
# inside thermal convection coefficient (W/m².K)
h_int = int(os.getenv('H_INT'))
# initial condition everywhere inside the grid (°C)
u_initial = int(os.getenv('U_INITIAL'))
# simulation duration (iteration number)
max_iter_time = int(os.getenv('MAX_ITER_TIME'))

# instatiate the method
job = Wall2dFDM(
        length=length, larger=larger, lambd=lambd, delta_xy=delta_xy, t_ext=t_ext, t_int=t_int,
        h_ext=h_ext, h_int=h_int, u_initial=u_initial, max_iter_time=max_iter_time
)

# plot the mesh grid
job.plot_grid_nodes()
# run the simulation
u2 = job.calculate_temperatures()
t2 = u2[-1]
# plot the heat map
job.plot_heat_map(t2)
# calculate the heat flow
q2 = round(job1.calculate_heat_flow(t1), 2)
print(f'heat flow : {q2} W')
```