# Import SMILEI parameters
from math import sqrt

# Simulation Parameters
L_x = 40.0  # Length of the simulation box in x-direction
L_y = 20.0  # Length of the simulation box in y-direction
nx = 400    # Number of cells in x-direction
ny = 200    # Number of cells in y-direction
timestep = 0.05  # Timestep, in units of the plasma frequency

# Particle and Injector Timing
particle_velocity = 0.1  # Speed of injected particles in x-direction
travel_time = L_x / particle_velocity
injection_duration = 1 / 3 * travel_time

# Main Simulation Block
Main(
    geometry = "2Dcartesian",
    interpolation_order = 2,
    cell_length = [L_x/nx, L_y/ny],
    grid_length  = [L_x, L_y],
    number_of_patches = [4, 4],
    timestep = timestep,
    simulation_time = travel_time * 4,  # Run for the travel time of the box
    EM_boundary_conditions = [["silver-muller", "reflective"], ["periodic", "periodic"]],
    random_seed = 0
)

# Species definition for electrons and ions
Species(
    name = "electrons",
    position_initialization = "random",
    momentum_initialization = "cold",
    particles_per_cell = 10,
    mass = 1.0,
    charge = -1.0,
    number_density = 0.1,
    boundary_conditions = [["remove", "reflective"], ["periodic", "periodic"]]
)

Species(
    name = "ions",
    position_initialization = "random",
    momentum_initialization = "cold",
    particles_per_cell = 10,
    mass = 1836.0,
    charge = 1.0,
    number_density = 0.1,
    boundary_conditions = [["remove", "reflective"], ["periodic", "periodic"]]
)

# High density injection for the first 1/6 of travel time
ParticleInjector(
    name = "high_density_injector",
    species = "ions",
    box_side = "xmin",
    mean_velocity = [particle_velocity, 0.0, 0.0],
    number_density = 0.15,
    time_envelope = tgaussian(start=0, duration=injection_duration, order=2)
)

# Medium density injection for the next 1/3 of travel time
ParticleInjector(
    name = "medium_density_injector",
    species = "ions",
    box_side = "xmin",
    mean_velocity = [particle_velocity, 0.0, 0.0],
    number_density = 0.1,
    time_envelope = tgaussian(start=injection_duration, duration=injection_duration, order=2)
)

# Low density injection for the final 1/2 of travel time
ParticleInjector(
    name = "low_density_injector",
    species = "ions",
    box_side = "xmin",
    mean_velocity = [particle_velocity, 0.0, 0.0],
    number_density = 0.05,
    time_envelope = tgaussian(start=injection_duration*2, duration=injection_duration, order=2)
)

# Diagnostics
DiagScalar(every = 100)  # Diagnostic for tracking scalar values

# Field diagnostic for electric and magnetic fields
DiagFields(
    every = 100,
    fields = ["Ex", "Ey", "Ez", "Bx", "By", "Bz"]
)

DiagTrackParticles(
    species = "electrons",
    attributes = ["x", "y"],
    every = 100
)

DiagTrackParticles(
    species = "ions",
    attributes = ["x", "y"],
    every = 100
)

# Particle diagnostic for observing particle distribution over time
DiagParticleBinning(
    deposited_quantity = "weight",
    every = 100,
    species = ["electrons", "ions"],
    axes = [
        ["x", 0, L_x, nx],
        ["y", 0, L_y, ny]
    ]
)
