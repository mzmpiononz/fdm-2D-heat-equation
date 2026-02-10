import numpy as np
import matplotlib.pyplot as plt

class Wall2dFDM:
    """
    Finite Difference Method with python:
    application to a 2D wall
    """ 
    def __init__(self, length, larger, lambd, delta_xy, t_ext, t_int, h_int, h_ext, u_initial, max_iter_time):
        """
        length : length of the wall (horizontal) (m)
        larger : larger of the wall (vertical) (m)
        lambd : thermal conductivity of the wall (W/m.K)
        delta_xy : mesh steps (m)
        t_ext : outside temperature (°C)
        t_int : inside temperature (°C)
        h_ext : outside thermal convection coefficient (W/m².K)
        h_int : inside thermal convection coefficient (W/m².K)
        u_initial : initial condition everywhere inside the grid (°C)
        max_iter_time = simulation duration
        """
        self.lambd = lambd
        self.delta_xy = delta_xy
        self.t_ext = t_ext
        self.t_int = t_int
        self.h_ext = h_ext
        self.h_int = h_int
        self.u_initial = u_initial
        self.max_iter_time = max_iter_time
        # number of rows 
        self.n_rows = len(np.arange(0, larger, self.delta_xy))
        # number of columns
        self.n_cols = len(np.arange(0, length, self.delta_xy))
        # number of nodes 
        self.n_nodes = self.n_rows * self.n_cols
        print(f'matrice shape : {self.n_rows}x{self.n_cols} = {self.n_nodes} nodes')

        # define some constants
        self.delta_t = (self.delta_xy ** 2)/(4 * self.lambd)
        self.gamma = (self.lambd * self.delta_t) / (self.delta_xy ** 2)
        self.teta_ext = (self.delta_xy/self.lambd)*self.h_ext
        self.teta_int = (self.delta_xy/self.lambd)*self.h_int

    def plot_grid_nodes(self):
        """
        plot the mesh grid, with (i,j) index for each node
        """
        # Generate and reshape the array
        arr = np.arange(1, self.n_nodes + 1).reshape((self.n_rows, self.n_cols))
        
        # Plotting
        plt.figure(figsize=(22, 8))
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                x = j
                y = -i  # flip y to simulate matrix-style row-major display
                value = arr[i, j]
                plt.plot(x, y, '.', color='blue')
                plt.text(x + 0.05, y + 0.1, f"({i},{j})", fontsize=9, color='black')
                plt.text(x + 0.05, y - 0.1, f"{value}", fontsize=9, color='darkred')
        plt.show()

    def plot_heat_map(self, u):
        """
        plot the heatmap of the results
        """
        plt.imshow(u, cmap='hot', origin='lower')  # Use 'hot' or 'jet' or other colormaps
        plt.colorbar(label='Temperature')
        plt.title(f"Temperature at t = {self.max_iter_time*self.delta_t:.3f} unit time")
        plt.xlabel('rows')
        plt.ylabel('cols')
        plt.show()

    def calculate_temperatures(self):
        """
        run the simulation to get temperatures for each nodes
        """
        # Initialize solution: the grid of u(k, i, j)
        u = np.empty((self.max_iter_time, self.n_rows, self.n_cols))   
        # set the initial condition
        u.fill(self.u_initial) 

        for k in range(0, self.max_iter_time-1, 1):
            for i in range(self.n_rows):
              for j in range(self.n_cols):
                  # convection h_ext + adiabatique 1
                  if i == 0 and j == 0:
                      uk_ip1_j = u[k][i+1][j]
                      uk_im1_j = ((1 - self.teta_ext)*u[k][i][j] + self.teta_ext*self.t_ext)
                      uk_i_jp1 = u[k][i][j+1]
                      uk_i_jm1 = u[k][i][j]
                      uk_i_j = u[k][i][j]
        
                  # adiabatique 1
                  elif i in range(1, self.n_rows-1) and j == 0:
                      uk_ip1_j = u[k][i+1][j]
                      uk_im1_j = u[k][i-1][j]
                      uk_i_jp1 = u[k][i][j+1]
                      uk_i_jm1 = u[k][i][j]
                      uk_i_j = u[k][i][j]
        
                  # adiabatique 1 + convection h_int
                  elif i == self.n_rows-1 and j == 0:
                      uk_ip1_j = ((1 - self.teta_int)*u[k][i][j] + self.teta_int*self.t_int)
                      uk_im1_j = u[k][i-1][j]
                      uk_i_jp1 = u[k][i][j+1]
                      uk_i_jm1 = u[k][i][j]
                      uk_i_j = u[k][i][j]
        
                  # convection h_int
                  elif i == self.n_rows-1 and j in range(1, self.n_cols-1):
                      uk_ip1_j = ((1 - self.teta_int)*u[k][i][j] + self.teta_int*self.t_int)
                      uk_im1_j = u[k][i-1][j]
                      uk_i_jp1 = u[k][i][j+1]
                      uk_i_jm1 = u[k][i][j-1]
                      uk_i_j = u[k][i][j]
        
                  # convection h_int + adiabatique 2 
                  elif i == self.n_rows-1 and j == self.n_cols-1:
                      uk_ip1_j = ((1 - self.teta_int)*u[k][i][j] + self.teta_int*self.t_int)
                      uk_im1_j = u[k][i-1][j]
                      uk_i_jp1 = u[k][i][j]
                      uk_i_jm1 = u[k][i][j-1]
                      uk_i_j = u[k][i][j]
        
                  # adiabatique 2
                  elif i in range(1, self.n_rows-1) and j == self.n_cols-1:
                      uk_ip1_j = u[k][i+1][j]
                      uk_im1_j = u[k][i-1][j]
                      uk_i_jp1 = u[k][i][j]
                      uk_i_jm1 = u[k][i][j-1]
                      uk_i_j = u[k][i][j]
        
                  # convection h_ext + adiabatique 2              
                  elif i == 0 and j == self.n_cols-1:
                      uk_ip1_j = u[k][i+1][j]
                      uk_im1_j = ((1 - self.teta_ext)*u[k][i][j] + self.teta_ext*self.t_ext)
                      uk_i_jp1 = u[k][i][j]
                      uk_i_jm1 = u[k][i][j-1]
                      uk_i_j = u[k][i][j]
        
                  # convection h_ext          
                  elif i == 0 and j in range(1, self.n_cols-1):
                      uk_ip1_j = u[k][i+1][j]
                      uk_im1_j = ((1 - self.teta_ext)*u[k][i][j] + self.teta_ext*self.t_ext)
                      uk_i_jp1 = u[k][i][j+1]
                      uk_i_jm1 = u[k][i][j-1]
                      uk_i_j = u[k][i][j]
        
                  # nodes in the middle
                  else:
                      uk_ip1_j = u[k][i+1][j]
                      uk_im1_j = u[k][i-1][j]
                      uk_i_jp1 = u[k][i][j+1]
                      uk_i_jm1 = u[k][i][j-1]
                      uk_i_j = u[k][i][j]
        
                  u[k+1, i, j] = self.gamma * (uk_ip1_j + uk_im1_j + uk_i_jp1 + uk_i_jm1 - 4*uk_i_j) + uk_i_j
        return u

        def calculate_heat_flow(self, u):
            """
        calculate the horizontal heat flow through the wall following the Fourier'sLaw
        """
        qx = -((u[1][:] - u[0][:]) / self.delta_xy)*self.lambd
        return np.sum(qx)*self.delta_xy