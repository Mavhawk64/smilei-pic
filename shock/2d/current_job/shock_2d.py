# Import SMILEI parameters
from math import sqrt

# def filter(particles):
#     return particles.px**2 + particles.py**2 + particles.pz**2 > 0


# Simulation Parameters
L_x = 40.0  # Length of the simulation box in x-direction
L_y = 20.0  # Length of the simulation box in y-direction
nx = 400  # Number of cells in x-direction
ny = 200  # Number of cells in y-direction
timestep = 0.01  # Timestep, in units of the plasma frequency
num_shocks = 1  # Number of shocks to inject

# Particle and Injector Timing
particle_velocity = 0.2  # Speed of injected particles in x-direction
travel_time = L_x / particle_velocity
injection_duration = 1 / 5 * travel_time

simulation_time = num_shocks * injection_duration  # Total simulation time
# travel_time + num_shocks * injection_duration  # Total simulation time

num_timesteps = int(simulation_time / timestep)  # Number of timesteps

# Main Simulation Block
Main(
    geometry="2Dcartesian",
    interpolation_order=2,
    cell_length=[L_x / nx, L_y / ny],
    grid_length=[L_x, L_y],
    number_of_patches=[4, 4],
    timestep=timestep,
    simulation_time=simulation_time,  # Run for the travel time of the box
    EM_boundary_conditions=[["silver-muller", "reflective"], ["periodic", "periodic"]],
    random_seed=0,
)

# Species definition for electrons and ions
Species(
    name="electrons",
    position_initialization="random",
    momentum_initialization="cold",
    particles_per_cell=64,
    mass=1.0,
    charge=-1.0,
    number_density=1,
    boundary_conditions=[["remove", "reflective"], ["periodic", "periodic"]],
)

Species(
    name="ions",
    position_initialization="random",
    momentum_initialization="cold",
    particles_per_cell=64,
    mass=1.0,
    charge=1.0,
    number_density=1,
    boundary_conditions=[["remove", "reflective"], ["periodic", "periodic"]],
)

# High density injection for the first 1/6 of travel time
for i in range(0, num_shocks):
    ParticleInjector(
        name=f"high_density_ion_{i}_injector",
        species="ions",
        box_side="xmin",
        mean_velocity=[particle_velocity, 0.0, 0.0],
        number_density=2.5,
        time_envelope=tgaussian(
            start=i * injection_duration, duration=injection_duration, order=2
        ),
    )
    ParticleInjector(
        name=f"high_density_ele_{i}_injector",
        species="electrons",
        box_side="xmin",
        mean_velocity=[particle_velocity, 0.0, 0.0],
        number_density=2.5,
        time_envelope=tgaussian(
            start=i * injection_duration, duration=injection_duration, order=2
        ),
    )

# Diagnostics
DiagScalar(every=100)  # Diagnostic for tracking scalar values

# Field diagnostic for electric and magnetic fields
DiagFields(every=100, fields=["Ex", "Ey", "Ez", "Bx", "By", "Bz"])

# Track particle positions and momenta for electrons
DiagTrackParticles(
    species="electrons",
    attributes=["px", "py"],
    every=num_timesteps // 2,
)

# Track particle positions and momenta for ions
DiagTrackParticles(species="ions", attributes=["px", "py"], every=num_timesteps // 2)

# Particle diagnostic for observing particle distribution over time
# DiagParticleBinning(
#     deposited_quantity="weight",
#     every=100,
#     species=["electrons", "ions"],
#     axes=[["x", 0, L_x, nx], ["y", 0, L_y, ny]],
# )
