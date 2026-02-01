#!/usr/bin/env python3
"""
Comprehensive demo of Photonics PDK capabilities.
"""

from photonics_pdk import *

print("=" * 70)
print(" " * 15 + "PHOTONICS PDK DEMONSTRATION")
print("=" * 70)
print()

# Section 1: Components
print("1. PHOTONIC COMPONENTS")
print("-" * 70)

wg = Waveguide("straight_wg", width=0.5, length=200.0)
print(f"   Waveguide: {wg.parameters['length']}µm × {wg.parameters['width']}µm")
print(f"   Loss: {wg.calculate_loss():.3f} dB")

dc = DirectionalCoupler("coupler_1", coupling_length=25.0, gap=0.15, coupling_ratio=0.5)
through, cross = dc.calculate_splitting_ratio()
print(f"   Directional Coupler: {through:.0%}/{cross:.0%} split")

ring = RingResonator("ring_1", radius=12.0, coupling_gap=0.18, width=0.5)
fsr = ring.calculate_fsr(effective_index=2.5)
q = ring.calculate_q_factor()
print(f"   Ring Resonator: R={ring.parameters['radius']}µm, FSR={fsr*1000:.2f}nm, Q={q:.0f}")
print()

# Section 2: Technology
print("2. TECHNOLOGY & MATERIALS")
print("-" * 70)

tech = get_soi_220nm_technology()
print(f"   Technology: {tech.name} @ {tech.wavelength}µm wavelength")

si = tech.get_material('Si')
sio2 = tech.get_material('SiO2')
print(f"   Core (Si): n={si.refractive_index}, dn/dT={si.thermal_coefficient:.2e}/K")
print(f"   Cladding (SiO2): n={sio2.refractive_index}, dn/dT={sio2.thermal_coefficient:.2e}/K")

neff = tech.calculate_effective_index('core', 0.5)
print(f"   Effective index @ w=0.5µm: {neff:.4f}")
print()

# Section 3: Design Rules
print("3. DESIGN RULE VALIDATION")
print("-" * 70)

dr = DesignRules("SOI220")
print(f"   Technology: {dr.technology_name}")

test_cases = [
    ("Width 0.5µm", dr.check_width(0.5)),
    ("Spacing 0.25µm", dr.check_spacing(0.25)),
    ("Bend radius 8µm", dr.check_bend_radius(8.0)),
    ("Coupling gap 0.15µm", dr.check_coupling_gap(0.15)),
]

for name, (valid, msg) in test_cases:
    status = "✓" if valid else "✗"
    print(f"   {status} {name}: {msg}")
print()

# Section 4: Calculations
print("4. OPTICAL CALCULATIONS")
print("-" * 70)

wavelength = 1.55
freq = wavelength_to_frequency(wavelength, 'um')
print(f"   λ = {wavelength}µm → f = {freq/1e12:.2f} THz")

power_dBm = 0
power_mW = dBm_to_watts(power_dBm) * 1000
print(f"   P = {power_dBm} dBm = {power_mW:.3f} mW")

from photonics_pdk.utils import calculate_phase_shift, calculate_mzi_transmission
import numpy as np

phase = calculate_phase_shift(100, 2.5, 1.55)
print(f"   Phase shift (100µm): {phase:.2f} rad = {np.degrees(phase):.1f}°")

trans_0 = calculate_mzi_transmission(0)
trans_pi = calculate_mzi_transmission(np.pi)
print(f"   MZI transmission: Δφ=0 → {trans_0:.2f}, Δφ=π → {trans_pi:.2f}")
print()

# Summary
print("=" * 70)
print(" " * 20 + "PDK SUMMARY")
print("=" * 70)
print(f"   Components implemented: 5 (Waveguide, Coupler, Y-Branch, MMI, Ring)")
print(f"   Materials defined: 4 (Si, SiO2, Si3N4, Air)")
print(f"   Design rules: {len(dr.list_rules())} rules enforced")
print(f"   Utility functions: 20+ calculation and conversion functions")
print("=" * 70)
print()
print("✓ Photonics PDK is ready for circuit design and simulation!")
print()
