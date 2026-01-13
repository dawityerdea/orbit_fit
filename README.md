# Orbit Fitting (FACET-II / SLAC)

This repository contains a lightweight example of my orbit-fitting workflow developed during my FACET-II internship at SLAC. The goal is to reconstruct the best-fit beam orbit from BPM (Beam Position Monitor) measurements using a linear transport model (R-matrices), and to support diagnostics such as estimating energy deviation from residuals in dispersive (spectrometer) regions.

## What’s in this repo
- **`orbit_fit.py`** — Core orbit-fitting routine (example implementation).
- **`example.ipynb`** — Small notebook showing how the fitting function can be called and how results can be inspected.

## What’s not included (and why)
The full production workflow used at SLAC depends on:
- Access to the **FACET-II control system / live model environment** (e.g., machine configuration and transport maps)
- **BPM datasets** and operational metadata that are not publicly shareable
- Site-specific tools, paths, and infrastructure available only on the FACET/SLAC computing environment

For these reasons, this repo is intentionally limited to a **portable example** that demonstrates the main ideas and structure of the algorithm without exposing protected machine data or internal tooling.

## Method overview (high level)
1. Build a linear model relating the initial orbit state to downstream BPM readings using transport matrices.
2. Solve the overdetermined system with **least-squares** (pseudo-inverse) to estimate the best-fit initial state.
3. Use residuals at spectrometer BPMs (high dispersion) to estimate **relative energy deviation**:
   \[
   x_{res} = x_{meas} - x_{fit}, \quad \delta \approx \frac{x_{res}}{\eta}
   \]
   where \( \eta \) is the dispersion (often related to \(R_{16}\)).

## How to run locally (example)
This example code is meant to be run with standard Python tools.

```bash
python -c "import orbit_fit; print('orbit_fit imported successfully')"
