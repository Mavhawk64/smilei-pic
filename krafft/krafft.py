# Import Smilei's library
from smilei import *

# Simulation parameters
electron_mass = 1.0
ion_mass = 1836.0  # Proton-to-electron mass ratio
electron_charge = -1.0
ion_charge = 1.0
Te_over_Ti = 10  # Electron-to-ion temperature ratio
nb_over_n0 = 5e-4  # Beam density relative to background plasma
vb_over_c = 0.25  # Drift velocity of beam as a fraction of the speed of light
vth_over_c = vb_over_c / 12.7  # Thermal velocity (calculated based on vb/vT)

# Domain parameters
Lx = 1448.0  # Normalized to Debye length
Ly = 1448.0  # Adjust according to simulation box requirements
Nx = 1024  # Number of grid points in x
Ny = 1024  # Number of grid points in y
Tsim = 15000.0  # Simulation time normalized to plasma frequency period
dt = 0.1  # Time step normalized to plasma frequency period

# Simulation setup
Main(
    geometry="2Dcartesian",
    interpolation_order=2,
    timestep=dt,
    simulation_time=Tsim,
    cell_length=[Lx / Nx, Ly / Ny],
    grid_length=[Lx, Ly],
    number_of_patches=[16, 16],
    time_fields_frozen=0.0,
    random_seed=smilei_mpi_rank,
    solve_poisson=False,
    print_every=100,
)

# Species: Background plasma electrons
Species(
    name="plasma_electrons",
    position_initialization="random",
    momentum_initialization="maxwellian",
    particles_per_cell=5400,
    mass=electron_mass,
    charge=electron_charge,
    number_density=1.0,
    temperature=[Te_over_Ti],  # Te based on Te/Ti ratio
    boundary_conditions=[["periodic", "periodic"], ["periodic", "periodic"]],
)

# Species: Background plasma ions
Species(
    name="plasma_ions",
    position_initialization="random",
    momentum_initialization="maxwellian",
    particles_per_cell=5400,
    mass=ion_mass,
    charge=ion_charge,
    number_density=1.0,
    temperature=[1.0],  # Ti set to 1 for simplicity
    boundary_conditions=[["periodic", "periodic"], ["periodic", "periodic"]],
)

# Species: Beam electrons
Species(
    name="beam_electrons",
    position_initialization="random",
    momentum_initialization="maxwellian",
    particles_per_cell=5400,
    mass=electron_mass,
    charge=electron_charge,
    number_density=nb_over_n0,
    mean_velocity=[vb_over_c, 0.0, 0.0],  # Drift along x-axis
    temperature=[vth_over_c**2],  # Adjust thermal velocity
    boundary_conditions=[["periodic", "periodic"], ["periodic", "periodic"]],
)

# Initialize electromagnetic fields
ExternalField(field="Ex", profile=0.0)
ExternalField(field="Ey", profile=0.0)
ExternalField(field="Ez", profile=0.0)

# Diagnostics for field energy, particle phase space, and density fluctuations
DiagScalar(every=100)

DiagFields(
    every=100, fields=["Ex", "Ey", "Ez", "Bx", "By", "Bz", "Rho_electron", "Rho_ion"]
)

DiagParticleBinning(
    deposited_quantity="weight",
    every=200,
    species=["beam_electrons"],
    axes=[["x", 0, Lx, 100], ["px", -5 * vb_over_c, 5 * vb_over_c, 100]],
)
