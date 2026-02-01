"""
Photonics PDK - A Process Design Kit library for photonics design and simulation.

This library provides foundational components, design rules, and utilities for
designing photonic integrated circuits.
"""

__version__ = "0.1.0"

from .components import (
    Component,
    Waveguide,
    DirectionalCoupler,
    YBranchSplitter,
    MMISplitter,
    RingResonator,
)

from .technology import (
    Technology,
    Layer,
    MaterialProperty,
)

from .design_rules import (
    DesignRules,
    check_minimum_width,
    check_minimum_spacing,
)

from .utils import (
    wavelength_to_frequency,
    frequency_to_wavelength,
    dBm_to_watts,
    watts_to_dBm,
)

__all__ = [
    # Core components
    "Component",
    "Waveguide",
    "DirectionalCoupler",
    "YBranchSplitter",
    "MMISplitter",
    "RingResonator",
    # Technology
    "Technology",
    "Layer",
    "MaterialProperty",
    # Design rules
    "DesignRules",
    "check_minimum_width",
    "check_minimum_spacing",
    # Utilities
    "wavelength_to_frequency",
    "frequency_to_wavelength",
    "dBm_to_watts",
    "watts_to_dBm",
]
