*****************************
Installing Required Packages
*****************************


AtomSK
=======

All installation instructions for AtomSK can be found on their documentation website https://atomsk.univ-lille.fr/dl.php .

.. note::

    It is highly recommended to install this program onto a linux operating system since it is
    significantly easier to install.

Ovito Visualization
====================

Ovito is used to view the crystals after creation as well as importing x, y, z atom posisitons into a python format.
Ovito Visualization tool can be downloaded through https://www.ovito.org .


Ovito API
==========

The Ovito API can be imported into python, which allows the user to import x, y, z atomic positions from the AtomSK
files.

.. code:: bash

    # Command to be run in terminal
    pip install ovito

.. note::

    The atomic positions returned from the Ovito API may not be the same as the x, y, z positions written in the file.
    Special interpreters are used in Ovitio to retrieve true atomic position according to all parameters specialized
    parameters dictated by the file type. These returned x, y, z positions should match the atomic position in the Ovito
    Visualization GUI.

ase
====

Some file reader

.. code:: python

    pip install ase

hycpy
======

Not 100% sure

.. code:: python

    # No idea on how to install

PYNX
====

The original importing script was given to the author in a Google Colab setting. Below is the Google Colab cell used
to import all required packges for pynx operation.

.. note::

    One can easily change this importer into a terminal importer by manually going through the script and
    installing packages as dictated.

.. code:: bash

    # Install every required package. Note that if you only want CUDA,
      # you can skip PyOpenCL, clFFT and gpyfft

    install_opencl = False

    try:
      # Do not reinstall if pynx is already present (useful for 'run all')
      import pynx

    except ModuleNotFoundError:

      # Base scientific computing packages and SILX
      !pip install numpy cython scipy matplotlib ipython scikit-image
      !pip install h5py hdf5plugin h5glance silx fabio

      # Install PyCUDA & PyOpenCL
      !pip install pycuda scikit-cuda

      # Install PyNX (nightly)
      !pip install http://ftp.esrf.fr/pub/scisoft/PyNX/pynx-devel-nightly.tar.bz2

      if install_opencl:
        !pip install opencl

        # Install clFFT
        !git clone https://github.com/clMathLibraries/clFFT.git --branch=v2.12.2
        !mkdir build
        !cd build && cmake ../clFFT/src && make all install

        # This is needed so that gpyfft can find libclFFT
        !ln -sf /usr/local/lib64/libclFFT.so.2 /usr/lib/

        # Install gpyfft (we need a specific version for PyNX compatibility)
        !git clone https://github.com/geggo/gpyfft.git
        !cd gpyfft && git checkout 2c07fa8e7674757 && python setup.py install

