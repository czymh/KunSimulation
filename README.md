## China Space Station Telescope (CSST) Emulator

A python package for CSST cosmological emulator.
This package is only dependent on `numpy`, `scipy` packages.
All the gaussian process trainings have been done in advance.
The whole package predicts the cosmological statistics [e.g., nonlinear matter power spectrum] with ~ **1 millisecond per cosmology**.

The parameter space are shown as followed:
| Parameter | Lower Limit | Upper Limit |
| --------- | ----------- | ----------- |
| $\Omega_b$          | 0.04  | 0.06    |
| $\Omega_{cb}$       | 0.24  | 0.40    |
| $H_0$               | 60    | 80      |
| $n_s$               | 0.92  | 1.00    |
| $A_s\times 10^{9}$  | 1.7   | 2.5     |
| $w$                 | -1.3  | -0.7    |
| $w_a$               | -0.5  | 0.5     |
| $\sum M_{\nu}$      | 0     | 0.3     |


## Acknowledgements
Feel free to contact <chyiru@sjtu.edu.cn> if you have any questions.  
