"""
Comprehensive test suite for Photonics PDK.

This test validates the main functionality of all PDK modules.
"""

import sys


def test_components():
    """Test component creation and basic operations."""
    print("\n=== Testing Components ===")
    from photonics_pdk import (
        Waveguide, DirectionalCoupler, YBranchSplitter, 
        MMISplitter, RingResonator
    )
    
    # Test Waveguide
    wg = Waveguide("wg1", 0.5, 100.0)
    assert wg.name == "wg1"
    assert wg.parameters['width'] == 0.5
    assert len(wg.ports) == 2
    loss = wg.calculate_loss()
    assert loss >= 0
    print(f"✓ Waveguide: created, loss={loss:.3f}dB")
    
    # Test DirectionalCoupler
    dc = DirectionalCoupler("dc1", 20.0, 0.2, 0.5)
    through, cross = dc.calculate_splitting_ratio()
    assert through + cross == 1.0
    assert len(dc.ports) == 4
    print(f"✓ DirectionalCoupler: created, splitting={through:.2f}/{cross:.2f}")
    
    # Test YBranchSplitter
    yb = YBranchSplitter("yb1", 1.0, 50.0)
    assert len(yb.ports) == 3
    print(f"✓ YBranchSplitter: created with 3 ports")
    
    # Test MMISplitter
    mmi = MMISplitter("mmi1", 6.0, 30.0, 1, 4)
    assert len(mmi.ports) == 5  # 1 input + 4 outputs
    print(f"✓ MMISplitter: created 1x4 configuration")
    
    # Test RingResonator
    ring = RingResonator("ring1", 10.0, 0.2)
    fsr = ring.calculate_fsr()
    q = ring.calculate_q_factor()
    assert fsr > 0
    assert q > 0
    print(f"✓ RingResonator: FSR={fsr:.4f}µm, Q={q:.0f}")
    

def test_technology():
    """Test technology definitions and materials."""
    print("\n=== Testing Technology ===")
    from photonics_pdk import (
        Technology, MaterialProperty, Layer,
        get_soi_220nm_technology, get_silicon_nitride_technology
    )
    
    # Test SOI220
    tech = get_soi_220nm_technology()
    assert tech.name == "SOI220"
    assert tech.wavelength == 1.55
    assert len(tech.materials) == 4
    assert len(tech.layers) == 4
    print(f"✓ SOI220 Technology: {len(tech.materials)} materials, {len(tech.layers)} layers")
    
    # Test material access
    si = tech.get_material('Si')
    assert si is not None
    assert si.refractive_index == 3.48
    print(f"✓ Silicon material: n={si.refractive_index}")
    
    # Test SiN technology
    tech_sin = get_silicon_nitride_technology()
    assert tech_sin.name == "SiN"
    core = tech_sin.get_layer('core')
    assert core.material == 'Si3N4'
    print(f"✓ SiN Technology: core material={core.material}")
    
    # Test effective index calculation
    neff = tech.calculate_effective_index('core', 0.5)
    assert 1.444 < neff < 3.48  # Between cladding and core
    print(f"✓ Effective index calculation: neff={neff:.4f}")
    
    # Test adding custom material
    custom_mat = MaterialProperty("Custom", 1.5, 0.0, 1e-4)
    tech.add_material('custom', custom_mat)
    assert tech.get_material('custom') == custom_mat
    print(f"✓ Custom material added")


def test_design_rules():
    """Test design rule checking."""
    print("\n=== Testing Design Rules ===")
    from photonics_pdk import (
        DesignRules, DesignRule,
        check_minimum_width, check_minimum_spacing
    )
    
    dr = DesignRules("SOI220")
    assert len(dr.rules) == 8
    print(f"✓ Design rules loaded: {len(dr.rules)} rules")
    
    # Test width checking
    valid, msg = dr.check_width(0.5)
    assert valid == True
    print(f"✓ Width check (0.5µm): {valid}")
    
    valid, msg = dr.check_width(0.3)
    assert valid == False
    print(f"✓ Width check (0.3µm): {valid} (expected)")
    
    # Test spacing checking
    valid, msg = dr.check_spacing(0.25)
    assert valid == True
    print(f"✓ Spacing check (0.25µm): {valid}")
    
    # Test bend radius
    valid, msg = dr.check_bend_radius(7.0)
    assert valid == True
    print(f"✓ Bend radius check (7.0µm): {valid}")
    
    # Test convenience functions
    assert check_minimum_width(0.5) == True
    assert check_minimum_spacing(0.3) == True
    print(f"✓ Convenience functions work")
    
    # Test adding custom rule
    custom_rule = DesignRule("test_rule", "minimum_width", 1.0, "core", "Test")
    dr.add_rule('test', custom_rule)
    assert dr.get_rule('test') == custom_rule
    print(f"✓ Custom rule added")


def test_utilities():
    """Test utility functions."""
    print("\n=== Testing Utilities ===")
    from photonics_pdk import (
        wavelength_to_frequency, frequency_to_wavelength,
        dBm_to_watts, watts_to_dBm
    )
    from photonics_pdk.utils import (
        dB_to_linear, linear_to_dB,
        calculate_phase_shift, calculate_mzi_transmission
    )
    import numpy as np
    
    # Test wavelength/frequency conversion
    wl = 1.55
    freq = wavelength_to_frequency(wl, 'um')
    wl_back = frequency_to_wavelength(freq, 'um')
    assert abs(wl - wl_back) < 1e-10
    print(f"✓ Wavelength/frequency conversion: {freq/1e12:.2f}THz")
    
    # Test power conversions
    p_watts = dBm_to_watts(0)
    assert abs(p_watts - 0.001) < 1e-10
    p_dBm = watts_to_dBm(p_watts)
    assert abs(p_dBm - 0) < 1e-10
    print(f"✓ Power conversion: 0dBm = {p_watts*1000}mW")
    
    # Test dB conversions
    linear = dB_to_linear(10)
    assert abs(linear - 10.0) < 1e-10
    db = linear_to_dB(linear)
    assert abs(db - 10.0) < 1e-10
    print(f"✓ dB conversion: 10dB = {linear} linear")
    
    # Test phase shift
    phase = calculate_phase_shift(100, 2.5, 1.55)
    assert phase > 0
    print(f"✓ Phase shift calculation: {phase:.2f}rad")
    
    # Test MZI transmission
    trans = calculate_mzi_transmission(0)
    assert abs(trans - 1.0) < 1e-10
    trans_pi = calculate_mzi_transmission(np.pi)
    assert abs(trans_pi - 0.0) < 1e-10
    print(f"✓ MZI transmission: 0rad={trans:.2f}, π rad={trans_pi:.2f}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Photonics PDK - Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        test_components()
        test_technology()
        test_design_rules()
        test_utilities()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
