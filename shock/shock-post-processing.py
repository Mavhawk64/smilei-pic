import os
import happi
import matplotlib.pyplot as plt
import numpy as np

# Open the simulation results
S = happi.Open(os.path.dirname(os.path.realpath(__file__)))

# Extract the Bx, By, and Bz fields
Bx_field_diag = S.Field(0, "Bx")
By_field_diag = S.Field(0, "By")
Bz_field_diag = S.Field(0, "Bz")

# Get data for each component and the timesteps for plotting
Bx_field_data = Bx_field_diag.getData()
By_field_data = By_field_diag.getData()
Bz_field_data = Bz_field_diag.getData()
timesteps = Bx_field_diag.getTimesteps()  # Assuming timesteps are consistent across diagnostics

# Calculate B^2 = Bx^2 + By^2 + Bz^2 / B_1^2 (B_1^2 taken from the first timestep)
B_squared = [Bx**2 + By**2 + Bz**2 for Bx, By, Bz in zip(Bx_field_data, By_field_data, Bz_field_data)]
B_1_squared = B_squared[0]  # Use first timestep as reference
log_B_squared = [np.log10(B / B_1_squared) for B in B_squared]

# Define x and y axes (based on simulation specifics)
x_min, x_max = 0, 2000  # Example values; adjust accordingly
t_min, t_max = 0, 400  # Example values; adjust accordingly

# Scaling factors for the top and right axes
scale_factor = 0.5  # Replace with appropriate scaling factor for x axis
time_scale = 0.2  # Replace with appropriate scaling factor for time axis

# Plot log(B^2/B_1^2)
plt.figure()
plt.imshow(log_B_squared, extent=[x_min, x_max, t_min, t_max], aspect="auto")
plt.colorbar(label=r"Log($B^2/B_1^2$)")

# Set labels for bottom and left axes
plt.xlabel(r"$x (\omega_{\text{pe}}/c)$")
plt.ylabel(r"$\omega_{\text{pe}}t$")

# Add secondary x-axis (top) and y-axis (right) with scaling
ax = plt.gca()
ax2 = ax.secondary_xaxis(
    "top", functions=(lambda x: x * scale_factor, lambda x: x / scale_factor)
)
ax2.set_xlabel(r"$x (\Omega_i/v_A)$")
ax3 = ax.secondary_yaxis(
    "right", functions=(lambda y: y * time_scale, lambda y: y / time_scale)
)
ax3.set_ylabel(r"$\Omega_i t$")

# Save plot
plt.savefig(f"{os.path.dirname(os.path.realpath(__file__))}/shock.png")

# Show plot
plt.show()
