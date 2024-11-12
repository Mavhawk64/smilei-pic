import os
import happi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Open the simulation results
S = happi.Open(os.path.dirname(os.path.realpath(__file__)))

# Access tracked particle data for a specific species, e.g., "electrons"
tracked_diag = S.TrackParticles("electrons", axes=["x", "y"])

# Get x and y positions across timesteps
data = tracked_diag.getData()
x_data = np.array(data["x"])  # Convert to numpy array for easier indexing
y_data = np.array(data["y"])
timesteps = tracked_diag.getTimesteps()

# Get axis boundaries from the diagnostic data
x_axis = tracked_diag.getAxis("x")
y_axis = tracked_diag.getAxis("y")

# Set up the figure and axis for animation
fig, ax = plt.subplots(figsize=(8, 6))
scat = ax.scatter([], [], s=0.001, color="green")
ax.set_xlim(x_axis[0], x_axis[1])  # Set x-axis boundaries
ax.set_ylim(y_axis[0], y_axis[1])  # Set y-axis boundaries
ax.set_xlabel("x position")
ax.set_ylabel("y position")
ax.set_title("Particle Positions in x-y Plane")

# Initialize the scatter plot
def init():
    empty_data = np.empty((0, 2))
    scat.set_offsets(empty_data)
    return scat,

# Update function to animate each frame
def update(frame):
    current_x = x_data[frame, :]  # Get x positions at current timestep
    current_y = y_data[frame, :]  # Get y positions at current timestep
    positions = np.column_stack((current_x, current_y))
    scat.set_offsets(positions)
    ax.set_title(f"Particle Positions at Timestep {timesteps[frame]}")
    return scat,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(timesteps), init_func=init, blit=True)

# Save the animation as an MP4 file
output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "electron_positions_xy.mp4")
ani.save(output_file, writer="ffmpeg", fps=10)
print(f"Animation saved as {output_file}")
