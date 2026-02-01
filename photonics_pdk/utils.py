"""
Utility functions for photonics calculations.

This module provides helper functions for common photonics calculations,
unit conversions, and data processing.
"""

import numpy as np
from typing import Union, Tuple


# Physical constants
SPEED_OF_LIGHT = 2.99792458e8  # m/s
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s


def wavelength_to_frequency(wavelength: Union[float, np.ndarray], 
                           unit: str = 'um') -> Union[float, np.ndarray]:
    """
    Convert wavelength to frequency.
    
    Args:
        wavelength: Wavelength value or array
        unit: Unit of wavelength ('um', 'nm', 'm')
        
    Returns:
        Frequency in Hz
    """
    # Convert to meters
    if unit == 'um':
        wavelength_m = wavelength * 1e-6
    elif unit == 'nm':
        wavelength_m = wavelength * 1e-9
    elif unit == 'm':
        wavelength_m = wavelength
    else:
        raise ValueError(f"Unknown unit: {unit}")
    
    frequency = SPEED_OF_LIGHT / wavelength_m
    return frequency


def frequency_to_wavelength(frequency: Union[float, np.ndarray], 
                           unit: str = 'um') -> Union[float, np.ndarray]:
    """
    Convert frequency to wavelength.
    
    Args:
        frequency: Frequency in Hz
        unit: Desired unit for wavelength ('um', 'nm', 'm')
        
    Returns:
        Wavelength in specified unit
    """
    wavelength_m = SPEED_OF_LIGHT / frequency
    
    # Convert from meters
    if unit == 'um':
        return wavelength_m * 1e6
    elif unit == 'nm':
        return wavelength_m * 1e9
    elif unit == 'm':
        return wavelength_m
    else:
        raise ValueError(f"Unknown unit: {unit}")


def dBm_to_watts(power_dBm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert power from dBm to watts.
    
    Args:
        power_dBm: Power in dBm
        
    Returns:
        Power in watts
    """
    return 10 ** ((power_dBm - 30) / 10)


def watts_to_dBm(power_watts: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert power from watts to dBm.
    
    Args:
        power_watts: Power in watts
        
    Returns:
        Power in dBm
    """
    return 10 * np.log10(power_watts) + 30


def dB_to_linear(dB_value: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert dB value to linear scale.
    
    Args:
        dB_value: Value in dB
        
    Returns:
        Linear value
    """
    return 10 ** (dB_value / 10)


def linear_to_dB(linear_value: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert linear value to dB scale.
    
    Args:
        linear_value: Linear value
        
    Returns:
        Value in dB
    """
    return 10 * np.log10(linear_value)


def calculate_group_index(n_eff: float, dn_eff_dlambda: float, 
                         wavelength: float) -> float:
    """
    Calculate group index from effective index and its wavelength derivative.
    
    Args:
        n_eff: Effective refractive index
        dn_eff_dlambda: Derivative of n_eff with respect to wavelength
        wavelength: Wavelength in micrometers
        
    Returns:
        Group index ng
    """
    ng = n_eff - wavelength * dn_eff_dlambda
    return ng


def calculate_group_velocity(ng: float, wavelength: float = 1.55) -> float:
    """
    Calculate group velocity from group index.
    
    Args:
        ng: Group index
        wavelength: Wavelength in micrometers (for reference)
        
    Returns:
        Group velocity in m/s
    """
    vg = SPEED_OF_LIGHT / ng
    return vg


def calculate_dispersion(d2n_dlambda2: float, wavelength: float, 
                        length: float) -> float:
    """
    Calculate group velocity dispersion (GVD).
    
    Args:
        d2n_dlambda2: Second derivative of effective index
        wavelength: Wavelength in micrometers
        length: Waveguide length in micrometers
        
    Returns:
        GVD in ps/nm
    """
    # Simplified GVD calculation
    lambda_m = wavelength * 1e-6
    length_m = length * 1e-6
    D = -(lambda_m / SPEED_OF_LIGHT) * d2n_dlambda2 * length_m
    return D * 1e12 / 1e9  # Convert to ps/nm


def calculate_coupling_coefficient(gap: float, wavelength: float = 1.55, 
                                  n_eff: float = 2.5) -> float:
    """
    Estimate coupling coefficient for a directional coupler.
    
    This is a simplified model. Real values require mode solver analysis.
    
    Args:
        gap: Gap between waveguides in micrometers
        wavelength: Wavelength in micrometers
        n_eff: Effective refractive index
        
    Returns:
        Coupling coefficient in 1/micrometer
    """
    # Simplified exponential decay model
    kappa = 0.5 * np.exp(-gap / (wavelength / (2 * np.pi * n_eff)))
    return kappa


def calculate_coupling_length(coupling_ratio: float, kappa: float) -> float:
    """
    Calculate required coupling length for desired coupling ratio.
    
    Args:
        coupling_ratio: Desired power coupling ratio (0 to 1)
        kappa: Coupling coefficient in 1/micrometer
        
    Returns:
        Coupling length in micrometers
    """
    if kappa == 0:
        raise ValueError("Coupling coefficient cannot be zero")
    
    # For 50/50 coupling: L = π/(4κ)
    # General case: L = arcsin(sqrt(coupling_ratio))/(2κ)
    length = np.arcsin(np.sqrt(coupling_ratio)) / (2 * kappa)
    return length


def calculate_phase_shift(length: float, n_eff: float, 
                         wavelength: float = 1.55) -> float:
    """
    Calculate phase shift in a waveguide.
    
    Args:
        length: Waveguide length in micrometers
        n_eff: Effective refractive index
        wavelength: Wavelength in micrometers
        
    Returns:
        Phase shift in radians
    """
    beta = 2 * np.pi * n_eff / wavelength
    phase = beta * length
    return phase


def calculate_mzi_transmission(phase_diff: float) -> float:
    """
    Calculate transmission of a Mach-Zehnder interferometer.
    
    Args:
        phase_diff: Phase difference between arms in radians
        
    Returns:
        Transmission (0 to 1)
    """
    transmission = 0.5 * (1 + np.cos(phase_diff))
    return transmission


def thermal_phase_shift(length: float, dn_dT: float, delta_T: float, 
                       wavelength: float = 1.55) -> float:
    """
    Calculate thermal phase shift in a waveguide.
    
    Args:
        length: Waveguide length in micrometers
        dn_dT: Thermo-optic coefficient in 1/K
        delta_T: Temperature change in Kelvin
        wavelength: Wavelength in micrometers
        
    Returns:
        Phase shift in radians
    """
    delta_phase = (2 * np.pi * length / wavelength) * dn_dT * delta_T
    return delta_phase


def calculate_q_from_linewidth(center_wavelength: float, 
                               linewidth: float) -> float:
    """
    Calculate quality factor from resonance linewidth.
    
    Args:
        center_wavelength: Center wavelength in micrometers
        linewidth: Full-width half-maximum linewidth in micrometers
        
    Returns:
        Quality factor Q
    """
    q_factor = center_wavelength / linewidth
    return q_factor


def calculate_extinction_ratio(P_on: float, P_off: float, 
                              unit: str = 'linear') -> float:
    """
    Calculate extinction ratio.
    
    Args:
        P_on: Power in ON state
        P_off: Power in OFF state
        unit: 'linear' or 'dB'
        
    Returns:
        Extinction ratio in specified unit
    """
    if unit == 'linear':
        return P_on / P_off
    elif unit == 'dB':
        return 10 * np.log10(P_on / P_off)
    else:
        raise ValueError(f"Unknown unit: {unit}")


def normalize_power(powers: np.ndarray) -> np.ndarray:
    """
    Normalize power array to sum to 1.
    
    Args:
        powers: Array of power values
        
    Returns:
        Normalized power array
    """
    total_power = np.sum(powers)
    if total_power == 0:
        raise ValueError("Total power is zero, cannot normalize")
    return powers / total_power
