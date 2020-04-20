**********************
Using pynx.scattering
**********************


Importing Modules
==================

.. code:: python

    # Default
    import numpy as np
    import matplotlib.pyplot as plt
    import tifffile as tif
    from tqdm import tqdm

    # Pynx
    from pynx.scattering import Fhkl_thread
    from pynx.utils.plot_utils import complex2rgbalog, complex2rgbalin

    # Ovito importer
    from ovito.io import import_file


Obtain Diffraction Pattern
===========================

.. code:: python

    input_file = './Au_cut_defect_reorient.cfg'


    # Importing xyz atom postions using ovito API
    pipeline = import_file(input_file)
    data = pipeline.source.compute(0)
    x = data.particles.positions[:, 0]
    y = data.particles.positions[:, 1]
    z = data.particles.positions[:, 2]

    # Au lattice constant
    lattice = 4.0782

    # Reflection to view
    hkl = [1, 1, 1]

    # Sampling rate
    nstep = 150

    dq = 1/lattice/nstep

    # Resolution of pattern
    nx = 64
    ny = 64
    nz = 64
    dqx = (np.arange(nx)[:,np.newaxis,np.newaxis]-nx/2)*dq
    dqy = (np.arange(ny)[np.newaxis,:,np.newaxis]-ny/2)*dq
    dqz = (np.arange(nz)[np.newaxis,np.newaxis,:]-nz/2)*dq

    qx = hkl[0]/lattice+dqx
    qy = hkl[1]/lattice+dqy
    qz = hkl[2]/lattice+dqz

    fhkl, dt =Fhkl_thread(qx,qy,qz,x,y,z,occ=None,gpu_name=gpu_name,language=gpu_language)
    intensity = abs(fhkl)**2

    central_slice = np.log(intensity[:,:,nz//2])


Obtain Inverse Fourier Transform
=================================

.. code:: python

    plt.figure(figsize=(14,6))

    # Along L
    plt.subplot(131)
    plt.imshow(np.log10(np.abs(fhkl).sum(axis=0)), extent=(sx.min()*a, sx.max()*a, sy.min()*a, sy.max()*a))
    plt.xlabel('H (r.l.u.)')
    plt.ylabel('K (r.l.u.)')
    plt.title("Integrated intensity along L")

    # Along K
    plt.subplot(132)
    plt.imshow(np.log10(np.abs(fhkl).sum(axis=1)), extent=(sx.min()*a, sx.max()*a, sy.min()*a, sy.max()*a))
    plt.xlabel('H (r.l.u.)')
    plt.ylabel('L (r.l.u.)')
    plt.title("Integrated intensity along K")

    # Complex Along L Center
    plt.subplot(133)
    plt.imshow(complex2rgbalog(fhkl[nsz//2]), extent=(sx.min()*a, sx.max()*a, sy.min()*a, sy.max()*a))
    plt.xlabel('H (r.l.u.)')
    plt.ylabel('K (r.l.u.)')
    plt.title("Complex amplitude in L center")

    # Inverse Fourier transform of calculated array - don't forget the fftshoft !
    rho = np.fft.fftshift(np.fft.ifftn(np.fft.fftshift(fhkl)))
    dy, dx = 1 / (ds * rho.shape[1]) * 1e9, 1 / (ds * rho.shape[2]) * 1e9
    plt.figure(figsize=(10,6))
    plt.subplot(121)
    plt.imshow(np.abs(rho.sum(axis=0)), extent=(-dx * nsx / 2, dx * nsx / 2, -dy * nsy / 2, dy * nsy / 2))
    plt.title("Integrated density along Z")
    plt.xlabel('X (nm)')
    plt.ylabel('Y (nm)')
    plt.xlim(x.min()*1e9*1.5, x.max()*1e9*1.5)
    plt.ylim(y.min()*1e9*1.2, y.max()*1e9*1.2)

    plt.subplot(122)
    plt.imshow(complex2rgbalin(rho[nsz//2]), extent=(-dx * nsx / 2, dx * nsx / 2, -dy * nsy / 2, dy * nsy / 2))
    plt.xlabel('X (nm)')
    plt.ylabel('Y (nm)')
    plt.xlim(x.min()*1e9*1.5, x.max()*1e9*1.5)
    plt.ylim(y.min()*1e9*1.2, y.max()*1e9*1.2)
    plt.title("Complex amplitude in Z center")


