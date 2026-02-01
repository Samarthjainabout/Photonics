"""
Design rules checking examples.

This example demonstrates how to use design rules to validate
photonic circuit layouts.
"""

from photonics_pdk import (
    DesignRules,
    DesignRule,
    check_minimum_width,
    check_minimum_spacing,
)


def main():
    print("=" * 60)
    print("Photonics PDK - Design Rules Examples")
    print("=" * 60)
    print()
    
    # Example 1: Create design rules instance
    print("1. Design Rules for SOI220")
    print("-" * 40)
    dr = DesignRules(technology_name="SOI220")
    print(f"{dr}")
    print(f"Total rules: {len(dr.list_rules())}")
    print()
    
    # List all rules
    print("Available design rules:")
    for key, rule in dr.list_rules().items():
        print(f"  {rule}")
    print()
    
    # Example 2: Width checking
    print("2. Waveguide Width Checking")
    print("-" * 40)
    test_widths = [0.3, 0.5, 1.0, 25.0]
    for width in test_widths:
        is_valid, message = dr.check_width(width)
        status = "✓" if is_valid else "✗"
        print(f"{status} Width {width}µm: {message}")
    print()
    
    # Example 3: Spacing checking
    print("3. Waveguide Spacing Checking")
    print("-" * 40)
    test_spacings = [0.1, 0.2, 0.5, 1.0]
    for spacing in test_spacings:
        is_valid, message = dr.check_spacing(spacing)
        status = "✓" if is_valid else "✗"
        print(f"{status} Spacing {spacing}µm: {message}")
    print()
    
    # Example 4: Bend radius checking
    print("4. Bend Radius Checking")
    print("-" * 40)
    test_radii = [3.0, 5.0, 10.0, 20.0]
    for radius in test_radii:
        is_valid, message = dr.check_bend_radius(radius)
        status = "✓" if is_valid else "✗"
        print(f"{status} Radius {radius}µm: {message}")
    print()
    
    # Example 5: Coupling gap checking
    print("5. Coupling Gap Checking")
    print("-" * 40)
    test_gaps = [0.05, 0.1, 0.3, 1.5]
    for gap in test_gaps:
        is_valid, message = dr.check_coupling_gap(gap)
        status = "✓" if is_valid else "✗"
        print(f"{status} Gap {gap}µm: {message}")
    print()
    
    # Example 6: Using convenience functions
    print("6. Convenience Functions")
    print("-" * 40)
    width = 0.45
    spacing = 0.25
    
    if check_minimum_width(width):
        print(f"✓ Width {width}µm passes design rules")
    else:
        print(f"✗ Width {width}µm fails design rules")
        
    if check_minimum_spacing(spacing):
        print(f"✓ Spacing {spacing}µm passes design rules")
    else:
        print(f"✗ Spacing {spacing}µm fails design rules")
    print()
    
    # Example 7: Adding custom rule
    print("7. Adding Custom Design Rule")
    print("-" * 40)
    custom_rule = DesignRule(
        name='max_mmi_width',
        rule_type='maximum_width',
        value=15.0,
        layer='core',
        description='Maximum MMI width for fabrication'
    )
    dr.add_rule('max_mmi_width', custom_rule)
    print(f"Added: {custom_rule}")
    print(f"Total rules: {len(dr.list_rules())}")
    print()
    
    print("=" * 60)
    print("All design rules examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
