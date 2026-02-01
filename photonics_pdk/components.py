"""
Core photonic components for the PDK library.

This module provides base classes and implementations for standard photonic
components used in integrated photonics.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np


class Component:
    """Base class for all photonic components."""
    
    def __init__(self, name: str, component_type: str):
        """
        Initialize a photonic component.
        
        Args:
            name: Unique identifier for the component
            component_type: Type of the component (e.g., 'waveguide', 'coupler')
        """
        self.name = name
        self.component_type = component_type
        self.parameters = {}
        self.ports = {}
        
    def add_port(self, port_name: str, position: Tuple[float, float], 
                 orientation: float = 0.0):
        """
        Add a port to the component.
        
        Args:
            port_name: Name of the port
            position: (x, y) coordinates of the port
            orientation: Angle of the port in degrees
        """
        self.ports[port_name] = {
            'position': position,
            'orientation': orientation
        }
        
    def get_parameters(self) -> Dict:
        """Return component parameters."""
        return self.parameters
        
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', type='{self.component_type}')"


class Waveguide(Component):
    """
    Waveguide component for photonic circuits.
    
    Represents a single-mode or multi-mode waveguide with specified dimensions.
    """
    
    def __init__(self, name: str, width: float, length: float, 
                 layer: str = "core", mode: str = "single"):
        """
        Initialize a waveguide.
        
        Args:
            name: Unique identifier
            width: Width of the waveguide in micrometers
            length: Length of the waveguide in micrometers
            layer: Layer name for fabrication
            mode: 'single' or 'multi' mode operation
        """
        super().__init__(name, "waveguide")
        self.parameters = {
            'width': width,
            'length': length,
            'layer': layer,
            'mode': mode,
        }
        
        # Add input and output ports
        self.add_port("input", (0, 0), 0)
        self.add_port("output", (length, 0), 0)
        
    def calculate_loss(self, wavelength: float = 1.55) -> float:
        """
        Calculate propagation loss in dB.
        
        Args:
            wavelength: Operating wavelength in micrometers
            
        Returns:
            Loss in dB
        """
        # Simplified loss model: 2 dB/cm for typical silicon waveguide
        loss_per_cm = 2.0
        return (self.parameters['length'] / 10000) * loss_per_cm


class DirectionalCoupler(Component):
    """
    Directional coupler for splitting/combining optical signals.
    
    A four-port device that couples light between two parallel waveguides.
    """
    
    def __init__(self, name: str, coupling_length: float, gap: float, 
                 coupling_ratio: float = 0.5):
        """
        Initialize a directional coupler.
        
        Args:
            name: Unique identifier
            coupling_length: Length of the coupling region in micrometers
            gap: Gap between waveguides in micrometers
            coupling_ratio: Power coupling ratio (0 to 1)
        """
        super().__init__(name, "directional_coupler")
        self.parameters = {
            'coupling_length': coupling_length,
            'gap': gap,
            'coupling_ratio': coupling_ratio,
        }
        
        # Add four ports
        self.add_port("input1", (0, gap/2), 0)
        self.add_port("input2", (0, -gap/2), 0)
        self.add_port("output1", (coupling_length, gap/2), 0)
        self.add_port("output2", (coupling_length, -gap/2), 0)
        
    def calculate_splitting_ratio(self) -> Tuple[float, float]:
        """
        Calculate the splitting ratio at output ports.
        
        Returns:
            Tuple of (through_port_ratio, cross_port_ratio)
        """
        coupling_ratio = self.parameters['coupling_ratio']
        through_ratio = 1 - coupling_ratio
        return (through_ratio, coupling_ratio)


class YBranchSplitter(Component):
    """
    Y-branch splitter for 1x2 signal splitting.
    
    A three-port device that splits input signal into two output arms.
    """
    
    def __init__(self, name: str, splitting_angle: float = 1.0, 
                 branch_length: float = 50.0):
        """
        Initialize a Y-branch splitter.
        
        Args:
            name: Unique identifier
            splitting_angle: Angle between output branches in degrees
            branch_length: Length of each branch in micrometers
        """
        super().__init__(name, "y_branch_splitter")
        self.parameters = {
            'splitting_angle': splitting_angle,
            'branch_length': branch_length,
            'splitting_ratio': 0.5,  # 50/50 split by default
        }
        
        # Calculate output port positions
        angle_rad = np.radians(splitting_angle / 2)
        y_offset = branch_length * np.tan(angle_rad)
        
        self.add_port("input", (0, 0), 0)
        self.add_port("output1", (branch_length, y_offset), splitting_angle/2)
        self.add_port("output2", (branch_length, -y_offset), -splitting_angle/2)


class MMISplitter(Component):
    """
    Multi-Mode Interference (MMI) splitter.
    
    A device that uses self-imaging in a multi-mode waveguide to split signals.
    """
    
    def __init__(self, name: str, width: float, length: float, 
                 num_inputs: int = 1, num_outputs: int = 2):
        """
        Initialize an MMI splitter.
        
        Args:
            name: Unique identifier
            width: Width of the MMI region in micrometers
            length: Length of the MMI region in micrometers
            num_inputs: Number of input ports
            num_outputs: Number of output ports
        """
        super().__init__(name, "mmi_splitter")
        self.parameters = {
            'width': width,
            'length': length,
            'num_inputs': num_inputs,
            'num_outputs': num_outputs,
        }
        
        # Add input ports
        for i in range(num_inputs):
            y_pos = (i - (num_inputs - 1) / 2) * (width / (num_inputs + 1))
            self.add_port(f"input{i+1}", (0, y_pos), 0)
            
        # Add output ports
        for i in range(num_outputs):
            y_pos = (i - (num_outputs - 1) / 2) * (width / (num_outputs + 1))
            self.add_port(f"output{i+1}", (length, y_pos), 0)


class RingResonator(Component):
    """
    Ring resonator for filtering and sensing applications.
    
    A circular waveguide coupled to a bus waveguide.
    """
    
    def __init__(self, name: str, radius: float, coupling_gap: float, 
                 width: float = 0.5):
        """
        Initialize a ring resonator.
        
        Args:
            name: Unique identifier
            radius: Radius of the ring in micrometers
            coupling_gap: Gap between ring and bus waveguide in micrometers
            width: Width of the ring waveguide in micrometers
        """
        super().__init__(name, "ring_resonator")
        self.parameters = {
            'radius': radius,
            'coupling_gap': coupling_gap,
            'width': width,
        }
        
        # Add ports for the bus waveguide
        self.add_port("input", (0, 0), 0)
        self.add_port("output", (2 * radius + 10, 0), 0)
        
    def calculate_fsr(self, effective_index: float = 2.5, 
                      wavelength: float = 1.55) -> float:
        """
        Calculate Free Spectral Range (FSR) of the resonator.
        
        Args:
            effective_index: Effective refractive index of the mode
            wavelength: Operating wavelength in micrometers
            
        Returns:
            FSR in micrometers
        """
        circumference = 2 * np.pi * self.parameters['radius']
        ng = effective_index  # Simplified: group index ≈ effective index
        fsr = wavelength ** 2 / (ng * circumference)
        return fsr
        
    def calculate_q_factor(self, propagation_loss_dB_per_cm: float = 2.0, 
                          coupling_coefficient: float = 0.1) -> float:
        """
        Calculate quality factor (Q) of the resonator.
        
        Args:
            propagation_loss_dB_per_cm: Waveguide loss in dB/cm
            coupling_coefficient: Coupling strength to bus waveguide
            
        Returns:
            Quality factor Q
        """
        circumference = 2 * np.pi * self.parameters['radius']
        # Convert loss to linear scale
        loss_per_round_trip = (circumference / 10000) * propagation_loss_dB_per_cm
        alpha = loss_per_round_trip / (10 * np.log10(np.e))
        
        # Simplified Q calculation
        wavelength = 1.55  # micrometers
        q_factor = 2 * np.pi * circumference / (wavelength * (alpha + coupling_coefficient))
        return q_factor
