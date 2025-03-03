Data Products
=============

Overview
--------

All simulations in the **Kun Universe** are generated by the modified version of the `Gadget-4` code with 129 different cosmologies.
Each simulation evolves :math:`3072^3` particles in a box of :math:`1~h^{-1}\mathrm{Gpc}`  on a side.
The massive neutrinos are incoporated through the Newtonian-motion gauge (detailed in `Heuschling et al. 2022 <https://ui.adsabs.harvard.edu/abs/2022JCAP...09..068H>`_).
All particles are initialized with the second-order Lagrangian Perturbation Theory (2LPT) at the fixed redshift :math:`z = 127`.
An isotropic glass-like distribution is applied to pre-initial loads.
At small scales, we fix the equivalent Plummer softening length to :math:`\epsilon = 8~h^{-1}\mathrm{kpc}` in comoving coordinates.
At large scales, the grid size for Particle-Mesh (PM) force calculation is fixed at :math:`N_\mathrm{grid}=6144`.
The maximum allowed time step is set to :math:`\mathrm{max}(\Delta \ln a) = 0.04`.

We output **12** snapshots at fixed redshifts of ``z = {3.00, 2.50, 2.00, 1.75, 1.50, 1.25, 1.00, 0.80, 0.50, 0.25, 0.10, 0.00}``.
The total storage size for the whole simulation suite is about **3.1 PB**.
The directory of each simulation output is named as ``csst/simulation/cXXXX/output/``, where ``XXXX`` is the cosmology index from 0000 - 0128.

The key data products are listed as follows. The corresponding Python scripts is available in the `github repo <https://github.com/czymh/csst-simulations-read>`_.

Particle Data
~~~~~~~~~~~~~

Snapshot
^^^^^^^^^

Full particle samples at **12** redshifts are saved in the HDF5 format, including positions, velocities, and particle IDs.
The positions and velocities are stored with the 32-bit float, and the particle IDs are stored with the 64-bit integer.
The directory is named as ``snapdir_xxx/snapshot_xxx.*.hdf5``, where ``xxx`` is the snapshot index from 000 - 011 and ``*`` is the file index from 0 - 1023.
The 1/64 downsampled particle samples are also available in the ``snapdir_xxx_down64/snapshot_xxx_down64.*.hdf5`` files, where ``xxx`` is the snapshot index from 000 - 011 and ``*`` is the file index from 0 - 1023.

Particle Lightcone
^^^^^^^^^^^^^^^^^^

We also save two on-the-fly pyramid particle light-cones up to :math:`z\leq 3` by tiling simulation boxes along the three main axes.
Each cone covers :math:`2116\,\mathrm{deg^2}`.
Two special line-of-sight directions :math:`\vec{n}_1 = \{ 0.8678,\ 0.3595,\ 0.3431 \}` and :math:`\vec{n}_2 = \{ 0.3595,\ 0.8678,\ 0.3431\}` are selected to dilute the structure repetitions caused by box replication.
Files for particle lightcone are saved in the HDF5 format.
The directory is named as ``lightcone_xx/conedir_yyyy/conesnap_yyyy.*.hdf5``, where ``xx`` is the lightcone index from 00 - 01, ``yyyy`` is the lightcone index starting from 0000, and `*` is the file index from 0 - 1023.

Halo Data
~~~~~~~~~

FOF-SubFind Halo
^^^^^^^^^^^^^^^^

The Friends-of-Friends (FOF) and SubFind halo/subhalo catalogs are saved in the HDF5 format.
It is stored in ``groups_xxx/fof_subhalo_tab_xxx.*.hdf5``, where ``xxx`` is the snapshot index from 000 - 011 and ``*`` is the file index from 0 - 1023.

Rockstar Halo
^^^^^^^^^^^^^

The Rockstar halo catalogs are saved in both ASCII format and HDF5 format.
The ASCII format is stored in ``groups_all_rockstar/out_x.list``, where ``x` is the snapshot index from 0 - 11.
The HDF5 format is stored in ``groups_xxx_rockstar/rockstar_tab_xxx.*.hdf5``, where ``xxx`` is the snapshot index from 000 - 011 and ``*`` is the file index from 0 - 63.

Field Data
~~~~~~~~~~

Matter Density Field
^^^^^^^^^^^^^^^^^^^^

The matter density field is saved in the HDF5 format for each snapshot.
The number of mesh grids is :math:`1536^3` and window function is the Cloud-in-Cell (CIC) scheme.
The files are named as ``mesh_xxx/mesh_xxx_CIC_Nmesh1536.*.hdf5``, where ``xxx`` is the snapshot index from 000 - 011 and ``*`` is the file index from 0 - 191.


Full-sky Mass Map
^^^^^^^^^^^^^^^^^

The full-sky mass map is saved in the HDF5 format with thickness of :math:`50~h^{-1}\mathrm{Mpc}`.
The files are named as ``mapsdir_xxx/maps_xxx.*.hdf5``, where ``xxx`` is the snapshot index starting from 000 but ending at different number for different cosmologies.
And ``*`` is the file index from 0 - 1023.
The map is schemed with the Healpix pixelization with the resolution of :math:`N_{\mathrm{side}} = 8192`.

Weak Lensing Convergence Map (Born Approximation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The weak lensing convergence map is saved in the binary format for :math:`z_s \in [0.5, 3.0]`  with distance interval of :math:`50~h^{-1}\mathrm{Mpc}`.
The files are named as ``kappas/kappa-nbox*-thickness50-8192.bin``, where ``*`` represents the used number of shells.
The corresponding source redshift is ``nbox * thickness``.

