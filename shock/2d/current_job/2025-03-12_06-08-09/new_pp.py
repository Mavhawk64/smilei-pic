import gc
import os

import happi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
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

# Access field data for Bx, By, and Bz over the grid and time
Bx_field_diag = S.Field(0, "Bx")
By_field_diag = S.Field(0, "By")
Bz_field_diag = S.Field(0, "Bz")

Bx_data = np.array(Bx_field_diag.getData())
By_data = np.array(By_field_diag.getData())
Bz_data = np.array(Bz_field_diag.getData())
B_magnitude = np.sqrt(Bx_data**2 + By_data**2 + Bz_data**2)

# Get axis boundaries
x_axis = [0, 40]
y_axis = [0, 20]

gc.collect()

# Add custom legends for particles
from matplotlib.lines import Line2D

# ==============================
# 2. Magnetic Field Magnitude Animation
# ==============================

fig2, ax2 = plt.subplots(figsize=(8, 6))
cmap = plt.get_cmap("coolwarm")
norm = Normalize(vmin=np.min(B_magnitude), vmax=np.max(B_magnitude))
im = ax2.imshow(
    B_magnitude[0].T,
    cmap=cmap,
    norm=norm,
    extent=[x_axis[0], x_axis[1], y_axis[0], y_axis[1]],
    aspect="auto",
)
ax2.set_xlabel("x position")
ax2.set_ylabel("y position")
ax2.set_title("Magnetic Field Magnitude B over time")
cbar = fig2.colorbar(im, ax=ax2)
cbar.set_label(r"$|B| = \sqrt{B_x^2 + B_y^2 + B_z^2}$")


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

gc.collect()

# # ==============================
# # 3. Power Spectrum Animation
# # ==============================

# fft_data = fftn(B_magnitude, axes=(1, 2))
# power_spectrum = np.abs(fft_data) ** 2
# freq_x = fftfreq(Bx_data.shape[1], d=(x_axis[1] - x_axis[0]) / Bx_data.shape[1])
# freq_y = fftfreq(By_data.shape[2], d=(y_axis[1] - y_axis[0]) / By_data.shape[2])

# fig_ps, ax_ps = plt.subplots(figsize=(8, 6))
# im_ps = ax_ps.imshow(
#     power_spectrum[0].T,
#     cmap="inferno",
#     extent=[freq_x.min(), freq_x.max(), freq_y.min(), freq_y.max()],
#     aspect="auto",
#     norm=Normalize(vmin=0, vmax=0.1),  # power_spectrum.max())
# )
# ax_ps.set_xlabel("Frequency (x)")
# ax_ps.set_ylabel("Frequency (y)")
# ax_ps.set_title("Power Spectrum Density")
# cbar_ps = fig_ps.colorbar(im_ps, ax=ax_ps)
# cbar_ps.set_label("Spectral Density")


# def update_ps(frame):
#     im_ps.set_data(power_spectrum[frame].T)
#     ax_ps.set_title(f"Power Spectrum at Timestep {timesteps[frame]}")
#     return (im_ps,)


# ps_animation = FuncAnimation(fig_ps, update_ps, frames=len(timesteps), blit=True)
# ps_output_file = os.path.join(
#     os.path.dirname(os.path.realpath(__file__)), "power_spectrum.mp4"
# )
# save_animation(ps_animation, ps_output_file, fps=10)
# print(f"Power Spectrum animation saved as {ps_output_file}")

# # ==============================
# # 4. Temperature Plot
# # ==============================

# # too expensive
# # electron_temperature = (px_data**2 + py_data**2).mean(axis=1)
# # ion_temperature = (ion_px_data**2 + ion_py_data**2).mean(axis=1)

# electron_temperature = []
# ion_temperature = []
# for i in range(len(timesteps)):
#     electron_temperature.append((px_data[i] ** 2 + py_data[i] ** 2).mean())
#     ion_temperature.append((ion_px_data[i] ** 2 + ion_py_data[i] ** 2).mean())

# fig_temp, ax_temp = plt.subplots(figsize=(8, 6))
# (line_e,) = ax_temp.plot([], [], label="Electron Temperature", color="magenta")
# (line_i,) = ax_temp.plot([], [], label="Ion Temperature", color="cyan")
# ax_temp.set_xlim(0, timesteps.max())
# ax_temp.set_ylim(0, max(electron_temperature.max(), ion_temperature.max()) * 1.1)
# ax_temp.set_xlabel("Time")
# ax_temp.set_ylabel("Temperature")
# ax_temp.legend()
# ax_temp.set_title("Temperature Evolution")


# def update_temp(frame):
#     line_e.set_data(timesteps[:frame], electron_temperature[:frame])
#     line_i.set_data(timesteps[:frame], ion_temperature[:frame])
#     return line_e, line_i


# temp_animation = FuncAnimation(fig_temp, update_temp, frames=len(timesteps), blit=True)
# temp_output_file = os.path.join(
#     os.path.dirname(os.path.realpath(__file__)), "temperature_evolution.mp4"
# )
# save_animation(temp_animation, temp_output_file, fps=10)
# print(f"Temperature animation saved as {temp_output_file}")
