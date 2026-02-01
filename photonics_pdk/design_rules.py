"""
Design rules for photonic circuit layout.

This module defines fabrication constraints, minimum feature sizes, and
design rule checking functions.
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class DesignRule:
    """Represents a single design rule constraint."""
    
    name: str
    rule_type: str  # 'minimum_width', 'minimum_spacing', 'maximum_width', etc.
    value: float  # in micrometers
    layer: Optional[str] = None
    description: str = ""
    
    def __repr__(self):
        layer_str = f", layer='{self.layer}'" if self.layer else ""
        return f"DesignRule(name='{self.name}', type='{self.rule_type}', value={self.value}µm{layer_str})"


class DesignRules:
    """
    Collection of design rules for a photonic technology.
    
    Provides design rule checking and validation for photonic layouts.
    """
    
    def __init__(self, technology_name: str = "SOI220"):
        """
        Initialize design rules.
        
        Args:
            technology_name: Name of the technology node
        """
        self.technology_name = technology_name
        self.rules = {}
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Initialize default design rules for SOI220 technology."""
        
        # Waveguide rules
        self.rules['wg_min_width'] = DesignRule(
            name='wg_min_width',
            rule_type='minimum_width',
            value=0.4,
            layer='core',
            description='Minimum waveguide width'
        )
        
        self.rules['wg_max_width'] = DesignRule(
            name='wg_max_width',
            rule_type='maximum_width',
            value=20.0,
            layer='core',
            description='Maximum waveguide width for single-mode operation'
        )
        
        # Spacing rules
        self.rules['wg_min_spacing'] = DesignRule(
            name='wg_min_spacing',
            rule_type='minimum_spacing',
            value=0.2,
            layer='core',
            description='Minimum spacing between waveguides'
        )
        
        # Bend radius
        self.rules['min_bend_radius'] = DesignRule(
            name='min_bend_radius',
            rule_type='minimum_radius',
            value=5.0,
            layer='core',
            description='Minimum bend radius to avoid excessive loss'
        )
        
        # Coupling gap
        self.rules['min_coupling_gap'] = DesignRule(
            name='min_coupling_gap',
            rule_type='minimum_spacing',
            value=0.1,
            layer='core',
            description='Minimum gap for directional couplers'
        )
        
        self.rules['max_coupling_gap'] = DesignRule(
            name='max_coupling_gap',
            rule_type='maximum_spacing',
            value=1.0,
            layer='core',
            description='Maximum practical coupling gap'
        )
        
        # Feature sizes
        self.rules['min_feature_size'] = DesignRule(
            name='min_feature_size',
            rule_type='minimum_width',
            value=0.1,
            layer='core',
            description='Minimum resolvable feature size'
        )
        
        # Taper rules
        self.rules['min_taper_length'] = DesignRule(
            name='min_taper_length',
            rule_type='minimum_length',
            value=10.0,
            layer='core',
            description='Minimum taper length for adiabatic transition'
        )
        
    def add_rule(self, key: str, rule: DesignRule):
        """
        Add a design rule.
        
        Args:
            key: Identifier for the rule
            rule: DesignRule instance
        """
        self.rules[key] = rule
        
    def get_rule(self, key: str) -> Optional[DesignRule]:
        """
        Get a design rule by key.
        
        Args:
            key: Rule identifier
            
        Returns:
            DesignRule or None if not found
        """
        return self.rules.get(key)
        
    def list_rules(self) -> Dict[str, DesignRule]:
        """Return all design rules."""
        return self.rules
        
    def check_width(self, width: float, layer: str = 'core') -> Tuple[bool, str]:
        """
        Check if a width meets design rules.
        
        Args:
            width: Width in micrometers
            layer: Layer name
            
        Returns:
            Tuple of (is_valid, message)
        """
        min_rule = self.get_rule('wg_min_width')
        max_rule = self.get_rule('wg_max_width')
        
        if min_rule and width < min_rule.value:
            return (False, f"Width {width}µm is below minimum {min_rule.value}µm")
            
        if max_rule and width > max_rule.value:
            return (False, f"Width {width}µm exceeds maximum {max_rule.value}µm")
            
        return (True, "Width is within design rules")
        
    def check_spacing(self, spacing: float, layer: str = 'core') -> Tuple[bool, str]:
        """
        Check if spacing meets design rules.
        
        Args:
            spacing: Spacing in micrometers
            layer: Layer name
            
        Returns:
            Tuple of (is_valid, message)
        """
        min_rule = self.get_rule('wg_min_spacing')
        
        if min_rule and spacing < min_rule.value:
            return (False, f"Spacing {spacing}µm is below minimum {min_rule.value}µm")
            
        return (True, "Spacing is within design rules")
        
    def check_bend_radius(self, radius: float) -> Tuple[bool, str]:
        """
        Check if bend radius meets design rules.
        
        Args:
            radius: Bend radius in micrometers
            
        Returns:
            Tuple of (is_valid, message)
        """
        min_rule = self.get_rule('min_bend_radius')
        
        if min_rule and radius < min_rule.value:
            return (False, f"Bend radius {radius}µm is below minimum {min_rule.value}µm")
            
        return (True, "Bend radius is within design rules")
        
    def check_coupling_gap(self, gap: float) -> Tuple[bool, str]:
        """
        Check if coupling gap meets design rules.
        
        Args:
            gap: Gap in micrometers
            
        Returns:
            Tuple of (is_valid, message)
        """
        min_rule = self.get_rule('min_coupling_gap')
        max_rule = self.get_rule('max_coupling_gap')
        
        if min_rule and gap < min_rule.value:
            return (False, f"Gap {gap}µm is below minimum {min_rule.value}µm")
            
        if max_rule and gap > max_rule.value:
            return (False, f"Gap {gap}µm exceeds maximum {max_rule.value}µm")
            
        return (True, "Coupling gap is within design rules")
        
    def __repr__(self):
        return f"DesignRules(technology='{self.technology_name}', rules={len(self.rules)})"


# Standalone checking functions for convenience
def check_minimum_width(width: float, technology_name: str = "SOI220") -> bool:
    """
    Check if width meets minimum design rule.
    
    Args:
        width: Width in micrometers
        technology_name: Technology node name
        
    Returns:
        True if valid, False otherwise
    """
    dr = DesignRules(technology_name)
    is_valid, _ = dr.check_width(width)
    return is_valid


def check_minimum_spacing(spacing: float, technology_name: str = "SOI220") -> bool:
    """
    Check if spacing meets minimum design rule.
    
    Args:
        spacing: Spacing in micrometers
        technology_name: Technology node name
        
    Returns:
        True if valid, False otherwise
    """
    dr = DesignRules(technology_name)
    is_valid, _ = dr.check_spacing(spacing)
    return is_valid


def check_minimum_bend_radius(radius: float, technology_name: str = "SOI220") -> bool:
    """
    Check if bend radius meets minimum design rule.
    
    Args:
        radius: Bend radius in micrometers
        technology_name: Technology node name
        
    Returns:
        True if valid, False otherwise
    """
    dr = DesignRules(technology_name)
    is_valid, _ = dr.check_bend_radius(radius)
    return is_valid
