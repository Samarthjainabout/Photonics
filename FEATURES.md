# Photonics PDK - Features Summary

## Overview
A comprehensive Process Design Kit (PDK) library for photonic integrated circuit design and simulation, implementing industry-standard components, material properties, and design rules.

## Module Structure

### 1. Components Module (`photonics_pdk/components.py`)
Base classes and implementations for photonic devices:

#### Base Component Class
- Port management system
- Parameter storage
- Extensible design pattern

#### Implemented Components
- **Waveguide**: Single/multi-mode with propagation loss calculation
- **Directional Coupler**: 4-port device with splitting ratio analysis
- **Y-Branch Splitter**: 1x2 symmetric splitter with configurable angle
- **MMI Splitter**: NxM multi-mode interference based splitter
- **Ring Resonator**: With FSR and Q-factor calculations

### 2. Technology Module (`photonics_pdk/technology.py`)
Material properties and fabrication parameters:

#### Materials Library
- Silicon (Si): n=3.48 @ 1550nm
- Silicon Dioxide (SiO2): n=1.444
- Silicon Nitride (Si3N4): n=2.0
- Air: n=1.0
- Thermo-optic coefficients included

#### Layer Stack
- Substrate, BOX, Core, Cladding layers
- SOI220 (220nm Silicon-on-Insulator)
- SiN (Silicon Nitride) platform

#### Features
- Effective index calculation
- Extensible material/layer system
- Pre-configured technology templates

### 3. Design Rules Module (`photonics_pdk/design_rules.py`)
Fabrication constraints and validation:

#### Default Rules (SOI220)
- Minimum waveguide width: 0.4 µm
- Maximum waveguide width: 20.0 µm
- Minimum spacing: 0.2 µm
- Minimum bend radius: 5.0 µm
- Coupling gap range: 0.1-1.0 µm
- Minimum feature size: 0.1 µm
- Minimum taper length: 10.0 µm

#### Validation Functions
- Width checking
- Spacing verification
- Bend radius validation
- Coupling gap constraints
- Extensible rule system

### 4. Utilities Module (`photonics_pdk/utils.py`)
Helper functions and calculations:

#### Unit Conversions
- Wavelength ↔ Frequency
- dBm ↔ Watts
- dB ↔ Linear scale

#### Optical Calculations
- Phase shift calculation
- Group index and velocity
- Coupling coefficient estimation
- MZI transmission
- Thermal phase shift
- Q-factor from linewidth
- Extinction ratio
- Power normalization

## Usage Examples

### Quick Start
```python
from photonics_pdk import *

# Create a waveguide
wg = Waveguide("wg1", width=0.5, length=100.0)
print(f"Loss: {wg.calculate_loss():.3f} dB")

# Create a ring resonator
ring = RingResonator("ring1", radius=10.0, coupling_gap=0.2)
fsr = ring.calculate_fsr()
q = ring.calculate_q_factor()

# Check design rules
dr = DesignRules("SOI220")
valid, msg = dr.check_width(0.5)

# Use utilities
freq = wavelength_to_frequency(1.55, 'um')
power_w = dBm_to_watts(0)  # 1 mW
```

## Testing

### Test Suite (`test_pdk.py`)
Comprehensive validation of:
- Component creation and calculations
- Technology and material access
- Design rule checking
- Utility functions
- All imports and exports

### Example Scripts
Located in `examples/`:
1. `basic_components.py` - Component usage
2. `technology_example.py` - Material and layer management
3. `design_rules_example.py` - Design rule checking
4. `utils_example.py` - Calculations and conversions

## Installation

```bash
pip install -e .
```

## Dependencies
- Python >= 3.7
- NumPy >= 1.19.0

## Quality Metrics
- ✓ All modules tested
- ✓ All examples run successfully
- ✓ Code review passed
- ✓ CodeQL security scan: 0 vulnerabilities
- ✓ Pythonic code style

## Future Extensions
Potential additions:
- Mode solver integration
- S-parameter calculations
- Layout generation (GDSII)
- Optical simulation backends
- Additional component types (modulators, detectors)
- Advanced material models
- Process variation analysis
