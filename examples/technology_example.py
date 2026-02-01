"""
Technology and material property examples.

This example demonstrates how to work with technology definitions,
material properties, and layer stacks.
"""

from photonics_pdk import (
    Technology,
    MaterialProperty,
    Layer,
    get_soi_220nm_technology,
    get_silicon_nitride_technology,
)


def main():
    print("=" * 60)
    print("Photonics PDK - Technology Examples")
    print("=" * 60)
    print()
    
    # Example 1: Using predefined SOI220 technology
    print("1. SOI220 Technology")
    print("-" * 40)
    tech_soi = get_soi_220nm_technology()
    print(f"Technology: {tech_soi}")
    print(f"Design wavelength: {tech_soi.wavelength} µm")
    print()
    
    # List materials
    print("Available materials:")
    for key, material in tech_soi.list_materials().items():
        print(f"  {key}: {material}")
    print()
    
    # List layers
    print("Layer stack:")
    for key, layer in tech_soi.list_layers().items():
        print(f"  {key}: {layer}")
    print()
    
    # Calculate effective index
    neff = tech_soi.calculate_effective_index(layer_key='core', width=0.5)
    print(f"Effective index (w=0.5µm): {neff:.4f}")
    print()
    
    # Example 2: Silicon Nitride technology
    print("2. Silicon Nitride Technology")
    print("-" * 40)
    tech_sin = get_silicon_nitride_technology()
    print(f"Technology: {tech_sin}")
    core_layer = tech_sin.get_layer('core')
    print(f"Core layer: {core_layer}")
    core_material = tech_sin.get_material(core_layer.material)
    print(f"Core material: {core_material}")
    print()
    
    # Example 3: Custom material
    print("3. Adding Custom Material")
    print("-" * 40)
    custom_material = MaterialProperty(
        name='Custom Polymer',
        refractive_index=1.5,
        extinction_coefficient=0.001,
        thermal_coefficient=5e-4
    )
    tech_soi.add_material('polymer', custom_material)
    print(f"Added custom material: {custom_material}")
    print(f"Total materials: {len(tech_soi.list_materials())}")
    print()
    
    # Example 4: Custom layer
    print("4. Adding Custom Layer")
    print("-" * 40)
    custom_layer = Layer(
        name='metal_layer',
        layer_number=30,
        thickness=0.5,
        material='polymer',
        purpose='heater'
    )
    tech_soi.add_layer('heater', custom_layer)
    print(f"Added custom layer: {custom_layer}")
    print(f"Total layers: {len(tech_soi.list_layers())}")
    print()
    
    # Example 5: Material properties comparison
    print("5. Material Properties Comparison")
    print("-" * 40)
    materials_to_compare = ['Si', 'SiO2', 'Si3N4']
    print(f"{'Material':<15} {'Index':<10} {'Thermo-optic (1/K)'}")
    print("-" * 45)
    for mat_key in materials_to_compare:
        mat = tech_soi.get_material(mat_key)
        print(f"{mat.name:<15} {mat.refractive_index:<10.3f} {mat.thermal_coefficient:.2e}")
    print()
    
    print("=" * 60)
    print("All technology examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
