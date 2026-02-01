"""
Utilities and calculations examples.

This example demonstrates various utility functions for photonics
calculations and unit conversions.
"""

from photonics_pdk import (
    wavelength_to_frequency,
    frequency_to_wavelength,
    dBm_to_watts,
    watts_to_dBm,
)

from photonics_pdk.utils import (
    dB_to_linear,
    linear_to_dB,
    calculate_coupling_coefficient,
    calculate_phase_shift,
    calculate_mzi_transmission,
    thermal_phase_shift,
    calculate_extinction_ratio,
)

import numpy as np


def main():
    print("=" * 60)
    print("Photonics PDK - Utilities Examples")
    print("=" * 60)
    print()
    
    # Example 1: Unit conversions
    print("1. Wavelength and Frequency Conversions")
    print("-" * 40)
    wavelength = 1.55  # micrometers
    freq = wavelength_to_frequency(wavelength, unit='um')
    print(f"Wavelength: {wavelength} µm")
    print(f"Frequency: {freq/1e12:.2f} THz")
    
    # Convert back
    wl_converted = frequency_to_wavelength(freq, unit='um')
    print(f"Converted back: {wl_converted:.2f} µm")
    print()
    
    # Example 2: Power conversions
    print("2. Power Unit Conversions")
    print("-" * 40)
    powers_dBm = [0, 10, -10, -30]
    print(f"{'dBm':<10} {'Watts':<15} {'mW':<10}")
    print("-" * 35)
    for p_dBm in powers_dBm:
        p_watts = dBm_to_watts(p_dBm)
        p_mW = p_watts * 1000
        print(f"{p_dBm:<10} {p_watts:<15.6e} {p_mW:<10.4f}")
    print()
    
    # Example 3: dB scale conversions
    print("3. dB Scale Conversions")
    print("-" * 40)
    linear_values = [1.0, 2.0, 10.0, 100.0]
    for val in linear_values:
        db_val = linear_to_dB(val)
        print(f"Linear: {val:<6.1f} → dB: {db_val:<6.2f}")
    print()
    
    # Example 4: Coupling calculations
    print("4. Coupling Coefficient Calculation")
    print("-" * 40)
    gaps = [0.1, 0.2, 0.3, 0.5]
    wavelength = 1.55
    print(f"Wavelength: {wavelength} µm")
    print(f"{'Gap (µm)':<12} {'Coupling κ (µm⁻¹)'}")
    print("-" * 30)
    for gap in gaps:
        kappa = calculate_coupling_coefficient(gap, wavelength)
        print(f"{gap:<12.2f} {kappa:<.4f}")
    print()
    
    # Example 5: Phase calculations
    print("5. Phase Shift Calculations")
    print("-" * 40)
    lengths = [10, 50, 100, 500]  # micrometers
    n_eff = 2.5
    wavelength = 1.55
    print(f"Effective index: {n_eff}")
    print(f"Wavelength: {wavelength} µm")
    print(f"{'Length (µm)':<15} {'Phase (rad)':<15} {'Phase (deg)'}")
    print("-" * 45)
    for length in lengths:
        phase = calculate_phase_shift(length, n_eff, wavelength)
        phase_deg = np.degrees(phase)
        print(f"{length:<15} {phase:<15.2f} {phase_deg:<.1f}")
    print()
    
    # Example 6: MZI transmission
    print("6. Mach-Zehnder Interferometer Transmission")
    print("-" * 40)
    phase_diffs = np.linspace(0, 2*np.pi, 9)
    print(f"{'Phase (rad)':<15} {'Phase (deg)':<15} {'Transmission'}")
    print("-" * 45)
    for phase in phase_diffs:
        transmission = calculate_mzi_transmission(phase)
        print(f"{phase:<15.2f} {np.degrees(phase):<15.1f} {transmission:<.3f}")
    print()
    
    # Example 7: Thermal phase shift
    print("7. Thermal Phase Shift")
    print("-" * 40)
    length = 100  # micrometers
    dn_dT = 1.86e-4  # Silicon thermo-optic coefficient (1/K)
    temp_changes = [1, 5, 10, 20]  # Kelvin
    print(f"Waveguide length: {length} µm")
    print(f"Thermo-optic coefficient: {dn_dT:.2e} 1/K")
    print(f"{'ΔT (K)':<12} {'Phase shift (rad)':<20} {'Phase shift (deg)'}")
    print("-" * 52)
    for dT in temp_changes:
        phase = thermal_phase_shift(length, dn_dT, dT, wavelength=1.55)
        print(f"{dT:<12} {phase:<20.3f} {np.degrees(phase):<.2f}")
    print()
    
    # Example 8: Extinction ratio
    print("8. Extinction Ratio Calculation")
    print("-" * 40)
    P_on = 1.0  # mW
    P_off_values = [0.01, 0.001, 0.0001]  # mW
    print(f"P_on: {P_on} mW")
    print(f"{'P_off (mW)':<15} {'ER (linear)':<15} {'ER (dB)'}")
    print("-" * 45)
    for P_off in P_off_values:
        er_linear = calculate_extinction_ratio(P_on, P_off, unit='linear')
        er_dB = calculate_extinction_ratio(P_on, P_off, unit='dB')
        print(f"{P_off:<15.4f} {er_linear:<15.0f} {er_dB:<.2f}")
    print()
    
    print("=" * 60)
    print("All utility examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
