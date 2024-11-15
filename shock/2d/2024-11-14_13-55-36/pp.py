import os
import happi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize

# Open the simulation results
print("Loading data from the simulation directory...")
S = happi.Open(os.path.dirname(os.path.realpath(__file__)))
print("Data loaded successfully!")

# Access tracked particle data for specific species: "electrons" and "ions"
print("Accessing tracked particle data for electrons and ions...")
ele_tracked_diag = S.TrackParticles("electrons", axes=["x", "y"])
ion_tracked_diag = S.TrackParticles("ions", axes=["x", "y"])
print("Tracked particle data accessed successfully!")

# Get x and y positions across timesteps for both electrons and ions
print("Extracting particle positions and timesteps...")
timesteps = ele_tracked_diag.getTimesteps()
print("DEBUG 0")
ele_data = ele_tracked_diag.getData(timestep=timesteps[0])  # Get data for the first timestep
print("DEBUG 1")
ion_data = ion_tracked_diag.getData()
print("DEBUG 2")
ele_x_data = np.array(ele_data["x"])  # Convert to numpy array for easier indexing
print("DEBUG 3")
ele_y_data = np.array(ele_data["y"])
print("DEBUG 4")
ion_x_data = np.array(ion_data["x"])
print("DEBUG 5")
ion_y_data = np.array(ion_data["y"])
print("Particle positions and timesteps extracted successfully!")

# Access field data for Bx, By, and Bz over the grid and time
print("Accessing magnetic field data...")
Bx_field_diag = S.Field(0, "Bx")
By_field_diag = S.Field(0, "By")
Bz_field_diag = S.Field(0, "Bz")
print("Magnetic field data accessed successfully!")

# Get data for B components and calculate B magnitude at each timestep
print("Extracting magnetic field data at each timestep...")
Bx_data = np.array(Bx_field_diag.getData()) # Check the orientation ([x, y] or [y, x])
By_data = np.array(By_field_diag.getData())
Bz_data = np.array(Bz_field_diag.getData())
B_magnitude = np.sqrt(Bx_data**2 + By_data**2 + Bz_data**2)
print("Magnetic field data extracted successfully!")

# Get axis boundaries from the particle diagnostic data
print("Extracting axis boundaries for the plots...")
x_axis = ele_tracked_diag.getAxis("x")
y_axis = ele_tracked_diag.getAxis("y")
print("Axis boundaries extracted successfully!")

# Particle Positions Animation
print("Creating particle positions animation...")
fig1, ax1 = plt.subplots(figsize=(8, 6))
electron_scat = ax1.scatter([], [], s=0.001, color="magenta", label="Electrons")
ion_scat = ax1.scatter([], [], s=0.001, color="cyan", label="Ions")
ax1.set_xlim(x_axis[0], x_axis[1])
ax1.set_ylim(y_axis[0], y_axis[1])
ax1.set_xlabel("x position")
ax1.set_ylabel("y position")
ax1.set_title("Particle Positions in x-y Plane")

# Add custom legends for particles
from matplotlib.lines import Line2D
custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor="magenta", markersize=5, label="Electrons"),
                 Line2D([0], [0], marker='o', color='w', markerfacecolor="cyan", markersize=5, label="Ions")]
ax1.legend(handles=custom_legend, loc="upper right")

def init_particles():
    empty_data = np.empty((0, 2))
    electron_scat.set_offsets(empty_data)
    ion_scat.set_offsets(empty_data)
    return electron_scat, ion_scat

def update_particles(frame):
    ele_current_x = ele_x_data[frame, :]
    ele_current_y = ele_y_data[frame, :]
    ion_current_x = ion_x_data[frame, :]
    ion_current_y = ion_y_data[frame, :]

    electron_positions = np.column_stack((ele_current_x, ele_current_y))
    ion_positions = np.column_stack((ion_current_x, ion_current_y))
    electron_scat.set_offsets(electron_positions)
    ion_scat.set_offsets(ion_positions)
    ax1.set_title(f"Particle Positions at Timestep {timesteps[frame]}")
    return electron_scat, ion_scat

particle_animation = FuncAnimation(fig1, update_particles, frames=len(timesteps), init_func=init_particles, blit=True)

# Save particle positions animation
particle_output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "electron_ion_positions_xy.mp4")
particle_animation.save(particle_output_file, writer="ffmpeg", fps=10)
print(f"Particle positions animation saved as {particle_output_file}")

# Magnetic Field Magnitude Animation with Ice Blue to Red Colormap
print("Creating magnetic field magnitude animation...")
fig2, ax2 = plt.subplots(figsize=(8, 6))
cmap = plt.get_cmap("coolwarm")  # Color map with ice blue to red gradient
norm = Normalize(vmin=np.min(B_magnitude), vmax=np.max(B_magnitude))  # Normalize color scale
im = ax2.imshow(B_magnitude[0].T, cmap=cmap, norm=norm, extent=[x_axis[0], x_axis[1], y_axis[0], y_axis[1]], aspect='auto')
ax2.set_xlabel("x position")
ax2.set_ylabel("y position")
ax2.set_title("Magnetic Field Magnitude B over time")
cbar = fig2.colorbar(im, ax=ax2)
cbar.set_label(r"$|B| = \sqrt{B_x^2 + B_y^2 + B_z^2}$")

def init_field():
    im.set_data(B_magnitude[0].T)  # Initialize B field to the first timestep
    return im,

def update_field(frame):
    im.set_data(B_magnitude[frame].T)  # Update with transposed data for correct orientation
    ax2.set_title(f"Magnetic Field Magnitude at Timestep {timesteps[frame]}")
    return im,

field_animation = FuncAnimation(fig2, update_field, frames=len(timesteps), init_func=init_field, blit=True)

# Save magnetic field magnitude animation
field_output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "magnetic_field_magnitude.mp4")
field_animation.save(field_output_file, writer="ffmpeg", fps=10)
print(f"Magnetic field magnitude animation saved as {field_output_file}")
