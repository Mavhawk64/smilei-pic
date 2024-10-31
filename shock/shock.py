# SMILEI input script for simulating a quasi-parallel collisionless shock
from math import cos, pi, sin, sqrt

# from smilei import *

# ------------------------------
# Constants and simulation parameters
# ------------------------------

# Fundamental constants
c = 1.0  # Speed of light in normalized units
e_charge = 1.0  # Elementary charge magnitude
epsilon0 = 1.0  # Vacuum permittivity
mu0 = 1.0  # Vacuum permeability (since c = 1/sqrt(mu0 * epsilon0))

# Mass ratios
me = 1.0  # Electron mass
mi = 64.0  # Ion mass (mass ratio mi/me = 64)

# Plasma parameters
n0 = 1.0  # Initial plasma density
Vin = 0.05  # Plasma inflow velocity (along x-axis)
vA = 0.01  # Alfvén velocity
theta = 20.0 * pi / 180.0  # Shock angle in radians (20 degrees)

# Temperatures
Te = 0.0016  # Electron temperature
Ti = 0.0016  # Ion temperature

# Derived quantities
B0 = vA * sqrt(mu0 * n0 * mi)  # Magnetic field magnitude
Bx0 = B0 * cos(theta)  # Bx component
Bz0 = B0 * sin(theta)  # Bz component
Ey0 = Vin * B0 * sin(theta)  # Motional electric field Ey

# Electron plasma and cyclotron frequencies
omega_pe = sqrt(n0 * e_charge**2 / (epsilon0 * me))  # Electron plasma frequency
omega_ce = e_charge * B0 / me  # Electron cyclotron frequency

# Ensure omega_pe / omega_ce = 12.5 as in the paper
desired_ratio = 12.5
omega_pe = desired_ratio * omega_ce  # Adjust omega_pe to satisfy the ratio

# Time step and spatial grid size
dx = 0.04  # Cell length (as per Debye length in the paper)
dt = 0.04  # Original time step
# dt = 0.1  # POC: Increase the timestep for faster computation
# Lx = 20000.0  # Original simulation box length
Lx = 2000.0  # POC: Reduce the simulation box length to 2000
Nx = int(Lx / dx)  # Number of grid points

# ------------------------------
# Main simulation parameters
# ------------------------------

Main(  # type: ignore
    geometry="1Dcartesian",
    interpolation_order=2,
    cell_length=[dx],
    grid_length=[Lx],
    # number_of_patches=[8],  # Original number of patches
    number_of_patches=[4],  # POC: Reduce number of patches for faster simulation
    timestep=dt,
    # simulation_time=1.77e5 * dt,  # Original total simulation time
    simulation_time=1.0e4 * dt,  # POC: Reduce total simulation time
    time_fields_frozen=0.0,
    EM_boundary_conditions=[["periodic"]],
    random_seed=smilei_mpi_rank,  # type: ignore
)

# ------------------------------
# Species definition
# ------------------------------

# Electrons
Species(  # type: ignore
    name="electron",
    position_initialization="random",
    momentum_initialization="maxwell-juettner",
    # particles_per_cell=128,  # Original number of particles per cell
    particles_per_cell=4,  # POC: Reduce number of particles per cell
    mass=me,
    charge=-e_charge,
    number_density=constant(n0),  # type: ignore
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Te, Te, Te],
    boundary_conditions=[
        ["remove", "remove"],  # Particles exit the simulation at boundaries
    ],
)

# Ions
Species(  # type: ignore
    name="ion",
    position_initialization="random",
    momentum_initialization="maxwell-juettner",
    # particles_per_cell=128,  # Original number of particles per cell
    particles_per_cell=4,  # POC: Reduce number of particles per cell
    mass=mi,
    charge=e_charge,
    number_density=constant(n0),  # type: ignore
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Ti, Ti, Ti],
    boundary_conditions=[
        [
            "remove",
            "reflective",
        ],  # Reflective boundary at the right for ions to create the shock
    ],
)

# ------------------------------
# Particle injection
# ------------------------------

# Electron injector
ParticleInjector(  # type: ignore
    species="electron",
    box_side="xmin",  # Inject from the left
    number_density=constant(n0),  # type: ignore
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Te, Te, Te],
)

# Ion injector
ParticleInjector(  # type: ignore
    species="ion",
    box_side="xmin",  # Inject from the left
    number_density=constant(n0),  # type: ignore
    mean_velocity=[Vin, 0.0, 0.0],
    temperature=[Ti, Ti, Ti],
)


# ------------------------------
# External fields
# ------------------------------

# Magnetic field components
ExternalField(field="Bx", profile=constant(Bx0))  # type: ignore
ExternalField(field="By", profile=constant(0))  # type: ignore
ExternalField(field="Bz", profile=constant(Bz0))  # type: ignore

# Motional electric field Ey
ExternalField(field="Ex", profile=constant(0))  # type: ignore
ExternalField(field="Ey", profile=constant(Ey0))  # type: ignore
ExternalField(field="Ez", profile=constant(0))  # type: ignore

# ------------------------------
# Diagnostics
# ------------------------------

# Field diagnostics
DiagFields(  # type: ignore
    every=100,  # Original diagnostic frequency
    fields=["Ex", "Ey", "Ez", "Bx", "By", "Bz"],
)

# Scalar diagnostics
DiagScalar(every=100)  # type: ignore

# Particle diagnostics
DiagParticleBinning(  # type: ignore
    deposited_quantity="weight",
    every=100,
    species=["electron", "ion"],
    axes=[
        ["x", 0.0, Lx, 500],  # POC: Reduce resolution for diagnostics
        ["px", -0.1, 0.1, 50],  # POC: Reduce resolution for diagnostics
    ],
)
