import os
import happi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Open the simulation results
S = happi.Open(os.path.dirname(os.path.realpath(__file__)))

# Access tracked particle data for specific species: "electrons" and "ions"
tracked_diag = S.TrackParticles("electrons", axes=["x", "y"])
ion_tracked_diag = S.TrackParticles("ions", axes=["x", "y"])

# Get x and y positions across timesteps for both electrons and ions
data = tracked_diag.getData()
ion_data = ion_tracked_diag.getData()
x_data = np.array(data["x"])  # Convert to numpy array for easier indexing
y_data = np.array(data["y"])
ion_x_data = np.array(ion_data["x"])
ion_y_data = np.array(ion_data["y"])
timesteps = tracked_diag.getTimesteps()

# Get axis boundaries from the diagnostic data
x_axis = tracked_diag.getAxis("x")
y_axis = tracked_diag.getAxis("y")

# Set up the figure and axis for animation
fig, ax = plt.subplots(figsize=(8, 6))
electron_scat = ax.scatter([], [], s=0.001, color="magenta", label="Electrons")
ion_scat = ax.scatter([], [], s=0.001, color="cyan", label="Ions")
ax.set_xlim(x_axis[0], x_axis[1])  # Set x-axis boundaries
ax.set_ylim(y_axis[0], y_axis[1])  # Set y-axis boundaries
ax.set_xlabel("x position")
ax.set_ylabel("y position")
ax.set_title("Particle Positions in x-y Plane")

# Add custom legends with colors for each particle type
from matplotlib.lines import Line2D
custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor="magenta", markersize=5, label="Electrons"),
                 Line2D([0], [0], marker='o', color='w', markerfacecolor="cyan", markersize=5, label="Ions")]
ax.legend(handles=custom_legend, loc="upper right")

# Initialize the scatter plots for electrons and ions
def init():
    empty_data = np.empty((0, 2))
    electron_scat.set_offsets(empty_data)
    ion_scat.set_offsets(empty_data)
    return electron_scat, ion_scat

# Update function to animate each frame
def update(frame):
    # Get current positions for electrons and ions at the current timestep
    current_x = x_data[frame, :]
    current_y = y_data[frame, :]
    ion_current_x = ion_x_data[frame, :]
    ion_current_y = ion_y_data[frame, :]

    # Stack positions and update scatter plots
    electron_positions = np.column_stack((current_x, current_y))
    ion_positions = np.column_stack((ion_current_x, ion_current_y))
    electron_scat.set_offsets(electron_positions)
    ion_scat.set_offsets(ion_positions)

    ax.set_title(f"Particle Positions at Timestep {timesteps[frame]}")
    return electron_scat, ion_scat

# Create the animation
ani = FuncAnimation(fig, update, frames=len(timesteps), init_func=init, blit=True)

# Save the animation as an MP4 file
output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "electron_ion_positions_xy.mp4")
ani.save(output_file, writer="ffmpeg", fps=10)
print(f"Animation saved as {output_file}")
