# pycolmapwrap
Python interface for COLMAP reconstructions, plus some convenient scripts for loading/modifying/converting reconstructions.

This code does not, however, run reconstruction -- it only provides a convenient interface for handling COLMAP's output.

## modified xvdp
* create setup installer
* moved to python > 3.3
* renamed pycolmap -> pycolmapwrap (to avoid confusion with https://github.com/colmap/pycolmap , python bindings for colmap

## dependencies
git clone https://github.com/xvdp/koreto && cd koreto && pip install . && cd -
git clone https://github.com/xvdp/vidi && cd vidi && pip install . && cd -


## colmap installation info
https://colmap.github.io/install.html

### Linux
sudo apt-get install \
    git \
    cmake \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev
sudo apt-get install libcgal-qt5-dev
sudo apt-get install libatlas-base-dev libsuitesparse-dev
git clone https://ceres-solver.googlesource.com/ceres-solver
cd ceres-solver
git checkout $(git describe --tags) # Checkout the latest release
mkdir build
cd build
cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF
make -j
sudo make install

git clone https://github.com/colmap/colmap.git
cd colmap
git checkout dev
mkdir build
cd build
cmake ..
make -j
sudo make install
