# smilei-pic

<!-- Installation -->
## Installation

One may follow this ChatGPT [guide](https://chatgpt.com/share/66ffeb30-e908-800e-b7c0-9e526559b260) to install Smilei-PIC on a Linux machine with various debugging and issues along the way.

1. Clone the repository

```bash
git clone https://github.com/SmileiPIC/Smilei.git
```

2. Clone this repository

```bash
git clone https://github.com/Mavhawk64/smilei-pic.git
```

3. Using either apt install or module load, install the following dependencies:

- make
- openmpi-bin
- libopenmpi-dev
- g++
- conda
- libhdf5-dev

4. Verify that the following dependencies are installed:

```bash
mpicxx --version
```

5. Install Python requirements:

```bash
conda create -n smilei python=3.11
conda activate smilei
conda install -c numpy matplotlib h5py
```

6. Set the following environment variables:

```bash
# SMILEI STUFF:

export PATH="/path/to/Smilei/repo/Smilei:$PATH"
export HDF5_ROOT_DIR=/usr/local/hdf5
export PATH=$HDF5_ROOT_DIR/bin:$PATH
export LD_LIBRARY_PATH=$HDF5_ROOT_DIR/lib:$LD_LIBRARY_PATH
export SMILEICXX=mpicxx
export HDF5_ROOT_DIR=/usr/local/hdf5
export CPPFLAGS=-I${HDF5_ROOT_DIR}/include
export LDFLAGS=-L${HDF5_ROOT_DIR}/lib
export PYTHONEXE=/root/anaconda3/envs/smilei/bin/python3
export PYTHONPATH="/root/anaconda3/envs/smilei/lib/python3.11/site-packages"
export LD_LIBRARY_PATH=/root/anaconda3/envs/smilei/lib:$LD_LIBRARY_PATH
```

and make changes where necessary.

7. Configure HDF5 with parallel I/O support:

```bash
cd /path/to/hdf5_build
CC=mpicc ./configure --prefix=$HDF5_ROOT_DIR --enable-parallel
make -j 4
make install
```

8. Build Smilei:

```bash
cd /path/to/Smilei
make clean
make machine=linux_x86_64_gnu -j 4
```

or simply run:

```bash
make
```

9. Source bash:

```bash
source ~/.bashrc
```

10. Run Smilei test:

```bash
./smilei /path/to/Smilei/benchmarks/tst1d_00_em_propagation.py
```

<!-- Comments / Installation Issues -->
## Comments / Installation Issues

If you have any issues, try using `make clean` inside Smilei to clean the build and then try building again. If you have any issues with the installation, please refer to the [official documentation](https://smileipic.github.io/Smilei/).
