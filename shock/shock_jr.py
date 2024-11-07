# SMILEI input script for a smaller test run
from math import cos, pi, sin, sqrt

# Define simulation output frequency for test
test_every = 100  # Increase diagnostic frequency for quicker test results

# ------------------------------
# Constants and simulation parameters
# ------------------------------

# Fundamental constants (remain the same)
c = 1.0  # Speed of light in normalized units
e_charge = 1.0  # Elementary charge magnitude
epsilon0 = 1.0  # Vacuum permittivity
mu0 = 1.0  # Vacuum permeability (since c = 1/sqrt(mu0 * epsilon0))

# Mass ratios
me = 1.0  # Electron mass
mi = 64.0  # Ion mass

# Plasma parameters
n0 = 1.0  # Initial plasma density
Vin = 0.05  # Plasma inflow velocity
vA = 0.01  # Alfvén velocity
theta = 20.0 * pi / 180.0  # Shock angle in radians

# Temperatures
Te = 0.0016  # Electron temperature
Ti = 0.0016  # Ion temperature

# Derived quantities
B0 = vA * sqrt(mu0 * n0 * mi)  # Magnetic field magnitude
Bx0 = B0 * cos(theta)  # Bx component
Bz0 = B0 * sin(theta)  # Bz component
Ey0 = Vin * B0 * sin(theta)  # Motional electric field Ey

# Plasma and cyclotron frequencies
# Electron plasma frequency
omega_pe = sqrt(n0 * e_charge**2 / (epsilon0 * me))
omega_ce = e_charge * B0 / me  # Electron cyclotron frequency

# Ensure omega_pe / omega_ce = 12.5 for consistency
desired_ratio = 12.5
omega_pe = desired_ratio * omega_ce

# Time step and spatial grid size
dx = 0.04  # Cell length (based on Debye length)
dt = 0.04  # Timestep
Lx = 500.0  # Reduced simulation box length for quick test
Nx = int(Lx / dx)  # Number of grid points

# ------------------------------
# Main simulation parameters
# ------------------------------

Main(
    geometry="1Dcartesian",
    interpolation_order=2,
    grid_length=[Lx],
    cell_length=[dx],
    timestep=dt,
    simulation_time=1.0e3 * dt,  # Reduced simulation time for test
    maxwell_solver="Yee",
    EM_boundary_conditions=[["reflective", "silver-muller"]],
    time_fields_frozen=0.0,
    number_of_patches=[4],  # Reduced for quick test
    cluster_width=5,
    print_every=10,
    random_seed=0,
)

Checkpoints(
    dump_step=test_every,
    dump_minutes=5,
    exit_after_dump=False,
    keep_n_dumps=1,
)

# ------------------------------
# Species definition
# ------------------------------

# Electrons
Species(
    name="electron",
    position_initialization="random",
    momentum_initialization="maxwell-juettner",
    particles_per_cell=16,  # Reduced particles per cell for test
    mass=me,
    charge=-e_charge,
    number_density=constant(n0),
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Te, Te, Te],
    boundary_conditions=[["remove", "remove"]],
)

# Ions
Species(
    name="ion",
    position_initialization="random",
    momentum_initialization="maxwell-juettner",
    particles_per_cell=16,
    mass=mi,
    charge=e_charge,
    number_density=constant(n0),
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Ti, Ti, Ti],
    boundary_conditions=[["remove", "reflective"]],
)

# ------------------------------
# Particle injection
# ------------------------------

ParticleInjector(
    species="electron",
    box_side="xmin",
    number_density=constant(n0),
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Te, Te, Te],
)

ParticleInjector(
    species="ion",
    box_side="xmin",
    number_density=constant(n0),
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Ti, Ti, Ti],
)

# ------------------------------
# External fields
# ------------------------------

ExternalField(field="Bx", profile=constant(Bx0))
ExternalField(field="By", profile=constant(0))
ExternalField(field="Bz", profile=constant(Bz0))

ExternalField(field="Ex", profile=constant(0))
ExternalField(field="Ey", profile=constant(Ey0))
ExternalField(field="Ez", profile=constant(0))

# ------------------------------
# Diagnostics
# ------------------------------

DiagFields(
    every=test_every,
    fields=["Ex", "Ey", "Ez", "Bx", "By", "Bz"],
)

DiagScalar(every=test_every)

DiagParticleBinning(
    deposited_quantity="weight",
    every=test_every,
    species=["electron", "ion"],
    axes=[
        ["x", 0.0, Lx, 50],  # Lower resolution on x-axis
        ["px", -0.1, 0.1, 10],  # Lower resolution for momentum
    ],
)
