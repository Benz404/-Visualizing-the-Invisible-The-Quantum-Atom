# ⚛️ Quantum Orbital Lab v3.0

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A mathematically rigorous, real-time 3D simulator designed to visualize the **Quantum Mechanical model** of the atom. This project bridges the gap between the classical Bohr model and modern Quantum Field Theory by visualizing the "fuzzy" nature of electron probability.



## 🔬 Scientific Overview

This simulator uses **Monte Carlo Sampling** to generate 3D point clouds based on the solutions to the Schrödinger Equation for Hydrogen-like atoms.

### Key Features
* **Precision Radial Math:** Implements **Associated Laguerre Polynomials** for principal quantum numbers $n=1$ through $n=4$.
* **Angular Harmonics:** Visualizes the geometric shapes of $s, p, d,$ and $f$ orbitals.
* **Phase Visualization:** Uses color-coding (Red/Blue) to represent the sign of the wavefunction ($\psi$), illustrating wave crests and troughs.
* **Dual-Plot Analysis:** Features a live-updating **Radial Probability Density** graph to show radial nodes and peaks.
* **Quantum Fluctuations:** Simulates vacuum energy jiggle to provide a "live" feel to the subatomic field.

## 🛠️ Installation & Usage

### Prerequisites
Ensure you have Python 3.10+ installed.

### Install Dependencies
```bash
pip install pygame pygame_gui numpy matplotlib
