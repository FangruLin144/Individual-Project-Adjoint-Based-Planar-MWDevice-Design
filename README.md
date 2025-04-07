# Microwave Device Optimization via Adjoint-Based Shape Sensitivity and Level Set Evolution

## Introduction

This repository contains the full Python implementation of an optimization framework for planar microwave devices using adjoint-based sensitivity analysis and level set shape evolution. The project is integrated with CST Studio Suite 2022 and written in Python 3.6.8.

The project goal is to automate and accelerate the design of planar microwave structures like couplers and resonators while meeting PCB fabrication constraints.

## Overview

*(pipeline diagram)*

The diagram shows the overall pipeline:

- CST simulations (forward and adjoint)  
- Shape gradient calculation  
- Level set boundary update  
- Gaussian smoothing and boundary clipping  
- CST model update

## Installation Instructions

1. **Clone this repository:**
   ```bash
   git clone https://github.com/FangruLin144/Y3_individual_project.git
   cd Y3_individual_project
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure CST Studio Suite is installed:**
   - CST 2022 or later is recommended.
   - CST must support COM automation (enabled by default on Windows), since the code uses a Python wrapper over CST's COM interface for scripting.

## Technical Details

### Equations

- **Adjoint-based shape derivative:**

  ```math
  \frac{d \mathcal{L}}{d \boldsymbol{p}} = \frac{dJ}{d\boldsymbol{p}} = \Re \left\{ -j\omega \int_{\Gamma_{\text{PEC}}} \left( \varepsilon \boldsymbol{E} \cdot \boldsymbol{E}^{\text{adj}} + \mu \boldsymbol{H} \cdot \boldsymbol{H}^{\text{adj}} \right) \, ds \right\}
  ```

- **Level set boundary evolution:**
  ```math
  \frac{\partial \Phi}{\partial t} + V |\nabla \Phi| = 0
  ```

- **Gaussian filtering:**
  ```math
  G(x) = \frac{1}{2\pi \sigma^2} \exp\left( -\frac{x^2}{2\sigma^2} \right)
  ```

### Key Files

- `run_optimization.py` — Entry point for full pipeline  
- `cst_wrapper/` — CST COM interface  
- `optimizer/` — Level set evolution and gradient calculations  
- `filters/` — Gaussian smoothing tools  
- `examples/` — Baseline CST project and configuration

## Known Issues and Future Improvements

- **Platform dependency:** Windows-only (due to CST COM interface)  
- **Slow CST startup:** First simulation may take up to 15 seconds  
- **Level set CFL condition:** The time step for level set updates is not automatically constrained to satisfy the Courant–Friedrichs–Lewy (CFL) condition, so the step size must be chosen manually to avoid instability  
- **Filter tuning:** Gaussian filter parameter σ may need empirical tuning per device

## Future Plans

- Parallelize simulation steps  
- Integrate filtering into the optimization loop

## Contact

Please raise issues or suggestions through the [GitHub Issues tab](https://github.com/FangruLin144/Y3_individual_project/issues).
