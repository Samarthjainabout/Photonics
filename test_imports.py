"""
Test script to verify all imports work correctly.
"""

def test_all_imports():
    """Test that all exports can be imported."""
    
    print("Testing imports from photonics_pdk...")
    
    # Core components
    from photonics_pdk import (
        Component,
        Waveguide,
        DirectionalCoupler,
        YBranchSplitter,
        MMISplitter,
        RingResonator,
    )
    print("✓ Component imports successful")
    
    # Technology
    from photonics_pdk import (
        Technology,
        Layer,
        MaterialProperty,
        get_soi_220nm_technology,
        get_silicon_nitride_technology,
    )
    print("✓ Technology imports successful")
    
    # Design rules
    from photonics_pdk import (
        DesignRules,
        DesignRule,
        check_minimum_width,
        check_minimum_spacing,
    )
    print("✓ Design rules imports successful")
    
    # Utilities
    from photonics_pdk import (
        wavelength_to_frequency,
        frequency_to_wavelength,
        dBm_to_watts,
        watts_to_dBm,
    )
    print("✓ Utilities imports successful")
    
    print("\nAll imports successful!")
    

if __name__ == "__main__":
    test_all_imports()
