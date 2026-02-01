# Photonics PDK

A comprehensive Process Design Kit (PDK) library for photonic integrated circuit design and simulation.

## Overview

This library provides foundational components, design rules, and utilities for designing photonic integrated circuits. It includes:

- **Core photonic components**: Waveguides, couplers, splitters, ring resonators
- **Technology definitions**: Material properties, layer stacks, fabrication parameters
- **Design rules**: Minimum feature sizes, spacing constraints, fabrication limits
- **Utilities**: Conversion functions, optical calculations, helper functions

## Installation

### From source

```bash
git clone https://github.com/Samarthjainabout/Photonics.git
cd Photonics
pip install -e .
```

### Requirements

- Python >= 3.7
- NumPy >= 1.19.0

## Quick Start

### Creating Components

```python
from photonics_pdk import Waveguide, DirectionalCoupler, RingResonator

# Create a waveguide
wg = Waveguide(name="wg1", width=0.5, length=100.0)
print(f"Waveguide loss: {wg.calculate_loss():.2f} dB")

# Create a directional coupler
coupler = DirectionalCoupler(
    name="dc1", 
    coupling_length=20.0, 
    gap=0.2, 
    coupling_ratio=0.5
)
through, cross = coupler.calculate_splitting_ratio()
print(f"Splitting ratio - Through: {through:.2f}, Cross: {cross:.2f}")

# Create a ring resonator
ring = RingResonator(name="ring1", radius=10.0, coupling_gap=0.2)
fsr = ring.calculate_fsr(effective_index=2.5, wavelength=1.55)
q_factor = ring.calculate_q_factor()
print(f"Ring FSR: {fsr:.4f} µm, Q-factor: {q_factor:.0f}")
```

### Working with Technology

```python
from photonics_pdk import Technology, get_soi_220nm_technology

# Use predefined SOI220 technology
tech = get_soi_220nm_technology()
print(f"Technology: {tech.name}")
print(f"Design wavelength: {tech.wavelength} µm")

# Access material properties
si_material = tech.get_material('Si')
print(f"Silicon refractive index: {si_material.refractive_index}")

# Calculate effective index
neff = tech.calculate_effective_index(layer_key='core', width=0.5)
print(f"Effective index: {neff:.3f}")
```

### Design Rule Checking

```python
from photonics_pdk import DesignRules

# Create design rules instance
dr = DesignRules(technology_name="SOI220")

# Check if design meets rules
is_valid, message = dr.check_width(0.5)
print(f"Width check: {message}")

is_valid, message = dr.check_spacing(0.15)
print(f"Spacing check: {message}")

is_valid, message = dr.check_bend_radius(7.0)
print(f"Bend radius check: {message}")
```

### Using Utilities

```python
from photonics_pdk import (
    wavelength_to_frequency,
    dBm_to_watts,
    calculate_coupling_coefficient
)

# Convert wavelength to frequency
freq = wavelength_to_frequency(1.55, unit='um')
print(f"Frequency: {freq/1e12:.2f} THz")

# Convert power units
power_watts = dBm_to_watts(0)  # 0 dBm
print(f"0 dBm = {power_watts*1000:.3f} mW")

# Calculate coupling coefficient
kappa = calculate_coupling_coefficient(gap=0.2, wavelength=1.55)
print(f"Coupling coefficient: {kappa:.4f} µm⁻¹")
```

## Available Components

### Waveguide
- Single-mode and multi-mode waveguides
- Configurable width and length
- Loss calculation

### Directional Coupler
- Four-port coupler for signal splitting/combining
- Adjustable coupling length and gap
- Splitting ratio calculation

### Y-Branch Splitter
- 1x2 signal splitting
- Configurable splitting angle
- Symmetric power splitting

### MMI Splitter
- Multi-mode interference based splitting
- Configurable NxM port configuration
- Compact footprint

### Ring Resonator
- Optical filtering and sensing
- FSR and Q-factor calculation
- Configurable radius and coupling

## Technology Features

### Predefined Materials
- Silicon (Si): n = 3.48 @ 1550nm
- Silicon Dioxide (SiO2): n = 1.444
- Silicon Nitride (Si3N4): n = 2.0
- Air: n = 1.0

### Layer Stack
- Substrate layer
- Buried oxide (BOX)
- Core layer (Si or SiN)
- Top cladding

### Technologies
- SOI220: 220nm Silicon-on-Insulator
- SiN: Silicon Nitride platform

## Design Rules

Default rules for SOI220 technology:

- **Minimum waveguide width**: 0.4 µm
- **Maximum waveguide width**: 20.0 µm (single-mode)
- **Minimum spacing**: 0.2 µm
- **Minimum bend radius**: 5.0 µm
- **Minimum coupling gap**: 0.1 µm
- **Maximum coupling gap**: 1.0 µm
- **Minimum feature size**: 0.1 µm
- **Minimum taper length**: 10.0 µm

## Utilities

### Unit Conversions
- Wavelength ↔ Frequency
- dBm ↔ Watts
- dB ↔ Linear scale

### Optical Calculations
- Group index and velocity
- Phase shift calculation
- Coupling coefficient estimation
- Q-factor from linewidth
- Extinction ratio
- Thermal phase shift

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Author

Samarth Jain

## Acknowledgments

This PDK library is designed for educational and research purposes in photonic integrated circuit design.