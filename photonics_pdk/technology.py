"""
Technology and process parameters for photonic PDK.

This module defines material properties, layer stacks, and fabrication parameters
for photonic integrated circuits.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MaterialProperty:
    """Material properties for photonic components."""
    
    name: str
    refractive_index: float
    extinction_coefficient: float = 0.0
    thermal_coefficient: float = 0.0  # dn/dT in 1/K
    
    def __repr__(self):
        return f"MaterialProperty(name='{self.name}', n={self.refractive_index})"


@dataclass
class Layer:
    """Represents a fabrication layer in the PDK."""
    
    name: str
    layer_number: int
    thickness: float  # in micrometers
    material: str
    purpose: str = "drawing"
    
    def __repr__(self):
        return f"Layer(name='{self.name}', layer={self.layer_number}, thickness={self.thickness}µm)"


class Technology:
    """
    Technology definition for a photonic PDK.
    
    Contains material properties, layer definitions, and process parameters
    for a specific fabrication technology.
    """
    
    def __init__(self, name: str, wavelength: float = 1.55):
        """
        Initialize a technology definition.
        
        Args:
            name: Name of the technology (e.g., 'SOI220', 'SiN')
            wavelength: Design wavelength in micrometers
        """
        self.name = name
        self.wavelength = wavelength
        self.materials = {}
        self.layers = {}
        self._initialize_default_materials()
        self._initialize_default_layers()
        
    def _initialize_default_materials(self):
        """Initialize default material properties."""
        # Silicon at 1550nm
        self.materials['Si'] = MaterialProperty(
            name='Silicon',
            refractive_index=3.48,
            extinction_coefficient=0.0,
            thermal_coefficient=1.86e-4
        )
        
        # Silicon Dioxide (SiO2)
        self.materials['SiO2'] = MaterialProperty(
            name='Silicon Dioxide',
            refractive_index=1.444,
            extinction_coefficient=0.0,
            thermal_coefficient=1.0e-5
        )
        
        # Silicon Nitride (Si3N4)
        self.materials['Si3N4'] = MaterialProperty(
            name='Silicon Nitride',
            refractive_index=2.0,
            extinction_coefficient=0.0,
            thermal_coefficient=2.45e-5
        )
        
        # Air
        self.materials['Air'] = MaterialProperty(
            name='Air',
            refractive_index=1.0,
            extinction_coefficient=0.0,
            thermal_coefficient=0.0
        )
        
    def _initialize_default_layers(self):
        """Initialize default layer stack for SOI (Silicon-on-Insulator)."""
        self.layers['substrate'] = Layer(
            name='substrate',
            layer_number=0,
            thickness=500.0,
            material='Si',
            purpose='substrate'
        )
        
        self.layers['box'] = Layer(
            name='buried_oxide',
            layer_number=1,
            thickness=2.0,
            material='SiO2',
            purpose='cladding'
        )
        
        self.layers['core'] = Layer(
            name='core',
            layer_number=10,
            thickness=0.22,
            material='Si',
            purpose='drawing'
        )
        
        self.layers['cladding'] = Layer(
            name='top_cladding',
            layer_number=20,
            thickness=2.0,
            material='SiO2',
            purpose='cladding'
        )
        
    def add_material(self, key: str, material: MaterialProperty):
        """
        Add a new material to the technology.
        
        Args:
            key: Identifier for the material
            material: MaterialProperty instance
        """
        self.materials[key] = material
        
    def get_material(self, key: str) -> Optional[MaterialProperty]:
        """
        Get a material property by key.
        
        Args:
            key: Material identifier
            
        Returns:
            MaterialProperty or None if not found
        """
        return self.materials.get(key)
        
    def add_layer(self, key: str, layer: Layer):
        """
        Add a new layer to the technology.
        
        Args:
            key: Identifier for the layer
            layer: Layer instance
        """
        self.layers[key] = layer
        
    def get_layer(self, key: str) -> Optional[Layer]:
        """
        Get a layer by key.
        
        Args:
            key: Layer identifier
            
        Returns:
            Layer or None if not found
        """
        return self.layers.get(key)
        
    def list_materials(self) -> Dict[str, MaterialProperty]:
        """Return all materials in the technology."""
        return self.materials
        
    def list_layers(self) -> Dict[str, Layer]:
        """Return all layers in the technology."""
        return self.layers
        
    def calculate_effective_index(self, layer_key: str = 'core', 
                                  width: float = 0.5) -> float:
        """
        Calculate effective refractive index for a waveguide.
        
        This is a simplified model. Real calculations require mode solvers.
        
        Args:
            layer_key: Layer to use for the core
            width: Width of the waveguide in micrometers
            
        Returns:
            Effective refractive index
        """
        layer = self.get_layer(layer_key)
        if not layer:
            raise ValueError(f"Layer '{layer_key}' not found")
            
        core_material = self.get_material(layer.material)
        if not core_material:
            raise ValueError(f"Material '{layer.material}' not found")
            
        # Simplified effective index calculation
        # Real value would come from mode solver
        n_core = core_material.refractive_index
        n_clad = self.materials['SiO2'].refractive_index
        
        # Approximate effective index (between core and cladding)
        neff = n_clad + (n_core - n_clad) * 0.75  # Simplified model
        return neff
        
    def __repr__(self):
        return (f"Technology(name='{self.name}', wavelength={self.wavelength}µm, "
                f"materials={len(self.materials)}, layers={len(self.layers)})")


# Predefined technology templates
def get_soi_220nm_technology() -> Technology:
    """
    Get standard 220nm Silicon-on-Insulator technology.
    
    Returns:
        Technology instance configured for SOI220
    """
    tech = Technology(name='SOI220', wavelength=1.55)
    # Default initialization already sets up SOI220
    return tech


def get_silicon_nitride_technology() -> Technology:
    """
    Get Silicon Nitride technology.
    
    Returns:
        Technology instance configured for SiN
    """
    tech = Technology(name='SiN', wavelength=1.55)
    
    # Override core layer with SiN
    tech.layers['core'] = Layer(
        name='core',
        layer_number=10,
        thickness=0.4,
        material='Si3N4',
        purpose='drawing'
    )
    
    return tech
