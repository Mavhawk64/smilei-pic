import gc
import os

import happi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.fft import fftfreq, fftn

gc.collect()


def save_animation(animation: FuncAnimation, filename: str, fps: int = 10):
    try:
        animation.save(filename, writer="ffmpeg", fps=fps)
        print(f"Animation saved as {filename}")
    except Exception as e:
        print(f"Failed to save {filename} as mp4 due to: {e}")
        print("Falling back to GIF format...")
        gif_filename = filename.replace(".mp4", ".gif")
        animation.save(gif_filename, writer="pillow", fps=fps)
        print(f"Animation saved as {gif_filename}")
        print("Please install ffmpeg to save animations in mp4 format.")


# Open the simulation results
S = happi.Open(os.path.dirname(os.path.realpath(__file__)))

# Get the TimeSteps from scalars/fields?
time = S.Scalar("time")
timesteps = time.getTimesteps()

tracked_diag = S.TrackParticles("electrons", axes=["px", "py"])
ion_tracked_diag = S.TrackParticles("ions", axes=["px", "py"])

# Get x, y, px, py positions and momenta across timesteps for both electrons and ions
data = tracked_diag.getData()
ion_data = ion_tracked_diag.getData()
px_data = np.nan_to_num(np.array(data["px"]))
py_data = np.nan_to_num(np.array(data["py"]))
ion_px_data = np.nan_to_num(np.array(ion_data["px"]))
ion_py_data = np.nan_to_num(np.array(ion_data["py"]))

# Access field data for Bx, By, and Bz over the grid and time
Bx_field_diag = S.Field(0, "Bx")
By_field_diag = S.Field(0, "By")
Bz_field_diag = S.Field(0, "Bz")

Bx_data = np.nan_to_num(np.array(Bx_field_diag.getData()))
By_data = np.nan_to_num(np.array(By_field_diag.getData()))
Bz_data = np.nan_to_num(np.array(Bz_field_diag.getData()))
B_magnitude = np.sqrt(Bx_data**2 + By_data**2 + Bz_data**2)

# Get axis boundaries
x_axis = [0, 40]
y_axis = [0, 20]

gc.collect()

# Define custom colormap
from matplotlib.colors import LinearSegmentedColormap

fixed_custom_cmap = LinearSegmentedColormap.from_list(
    "fixed_custom_cmap",
    [
        ("black"),  # 0 -> Black
        ("#00265b"),  # 10^-3 -> Deep Blue
        ("#00965f"),  # 10^-2 -> Green
        ("#ff0000"),  # 10^-1 -> Red
        ("#ffff00"),  # 10^0 -> Yellow
    ],
)

# ==============================
# 1. Magnetic Field Magnitude Animation
# ==============================

fig2, ax2 = plt.subplots(
    figsize=(10, 5)
)  # Set figure size to maintain a 2:1 aspect ratio

# Use logarithmic normalization
norm = LogNorm(vmin=1e-3, vmax=1)

im = ax2.imshow(
    B_magnitude[0].T,
    cmap=fixed_custom_cmap,
    norm=norm,
    extent=[x_axis[0], x_axis[1], y_axis[0], y_axis[1]],
    origin="lower",
    aspect="auto",
)

ax2.set_xlim(x_axis)
ax2.set_ylim(y_axis)
ax2.set_xlabel("x position")
ax2.set_ylabel("y position")
ax2.set_title("Magnetic Field Magnitude B over time")

# Set log-scale colorbar
cbar = fig2.colorbar(im, ax=ax2, orientation="vertical")
cbar.set_label(r"$|B| = \sqrt{B_x^2 + B_y^2 + B_z^2}$")
cbar.set_ticks([1e-3, 1e-2, 1e-1, 1e0])
cbar.set_ticklabels(["$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$"])


def init_field():
    im.set_data(B_magnitude[0].T)
    return (im,)


def update_field(frame):
    im.set_data(B_magnitude[frame].T)
    ax2.set_title(f"Magnetic Field Magnitude at Timestep {timesteps[frame]}")
    return (im,)


field_animation = FuncAnimation(
    fig2, update_field, frames=len(timesteps), init_func=init_field, blit=True
)

field_output_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "magnetic_field_magnitude.mp4"
)
save_animation(field_animation, field_output_file, fps=10)
print(f"Magnetic field magnitude animation saved as {field_output_file}")

# ==============================
# 2. Energy Histogram Animation
# ==============================

e_energy = 0.5 * S.namelist.Species[0].mass * (px_data**2 + py_data**2)
i_energy = 0.5 * S.namelist.Species[1].mass * (ion_px_data**2 + ion_py_data**2)

# Determine bin count using Sturges' rule
num_bins = int(np.ceil(1 + np.log2(len(e_energy[0]))))

fig3, ax3 = plt.subplots(figsize=(8, 5))

# Set fixed axis limits
energy_min = min(e_energy.min(), i_energy.min())
energy_max = max(e_energy.max(), i_energy.max())
ax3.set_xlim(energy_min, energy_max)
ax3.set_ylim(0, None)  # Auto-scale y-axis


# Animation update function
def update_hist(frame):
    ax3.clear()
    ax3.hist(e_energy[frame], bins=num_bins, color="cyan", alpha=0.5, label="Electrons")
    ax3.hist(i_energy[frame], bins=num_bins, color="magenta", alpha=0.5, label="Ions")
    ax3.set_xlim(energy_min, energy_max)
    ax3.set_ylim(0, None)
    ax3.set_xlabel("Energy")
    ax3.set_ylabel("Counts")
    ax3.set_title(
        f"Energy Distribution at Timestep {int(frame / (len(e_energy)-1) * max(timesteps))}"
    )
    ax3.legend()


hist_animation = FuncAnimation(fig3, update_hist, frames=len(e_energy), blit=False)

hist_output_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "energy_histogram.mp4"
)
save_animation(hist_animation, hist_output_file, fps=5)
print(f"Energy histogram animation saved as {hist_output_file}")

gc.collect()
