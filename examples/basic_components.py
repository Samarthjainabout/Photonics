"""
Basic component usage examples.

This example demonstrates how to create and use basic photonic components
from the PDK library.
"""

from photonics_pdk import (
    Waveguide,
    DirectionalCoupler,
    YBranchSplitter,
    MMISplitter,
    RingResonator,
)


def main():
    print("=" * 60)
    print("Photonics PDK - Basic Component Examples")
    print("=" * 60)
    print()
    
    # Example 1: Waveguide
    print("1. Waveguide Example")
    print("-" * 40)
    wg = Waveguide(name="wg1", width=0.5, length=100.0, layer="core")
    print(f"Created: {wg}")
    print(f"Parameters: {wg.get_parameters()}")
    print(f"Propagation loss @ 1.55µm: {wg.calculate_loss():.3f} dB")
    print(f"Ports: {list(wg.ports.keys())}")
    print()
    
    # Example 2: Directional Coupler
    print("2. Directional Coupler Example")
    print("-" * 40)
    coupler = DirectionalCoupler(
        name="dc1",
        coupling_length=20.0,
        gap=0.2,
        coupling_ratio=0.5
    )
    print(f"Created: {coupler}")
    through, cross = coupler.calculate_splitting_ratio()
    print(f"Splitting ratio:")
    print(f"  Through port: {through:.1%}")
    print(f"  Cross port: {cross:.1%}")
    print(f"Ports: {list(coupler.ports.keys())}")
    print()
    
    # Example 3: Y-Branch Splitter
    print("3. Y-Branch Splitter Example")
    print("-" * 40)
    y_splitter = YBranchSplitter(
        name="y1",
        splitting_angle=1.0,
        branch_length=50.0
    )
    print(f"Created: {y_splitter}")
    print(f"Parameters: {y_splitter.get_parameters()}")
    print(f"Splitting ratio: 50/50 (symmetric)")
    print(f"Ports: {list(y_splitter.ports.keys())}")
    print()
    
    # Example 4: MMI Splitter
    print("4. MMI Splitter Example")
    print("-" * 40)
    mmi = MMISplitter(
        name="mmi1",
        width=6.0,
        length=30.0,
        num_inputs=1,
        num_outputs=4
    )
    print(f"Created: {mmi}")
    print(f"Configuration: {mmi.parameters['num_inputs']}x{mmi.parameters['num_outputs']}")
    print(f"Ports: {list(mmi.ports.keys())}")
    print()
    
    # Example 5: Ring Resonator
    print("5. Ring Resonator Example")
    print("-" * 40)
    ring = RingResonator(
        name="ring1",
        radius=10.0,
        coupling_gap=0.2,
        width=0.5
    )
    print(f"Created: {ring}")
    print(f"Parameters: {ring.get_parameters()}")
    
    # Calculate performance metrics
    effective_index = 2.5
    wavelength = 1.55
    fsr = ring.calculate_fsr(effective_index=effective_index, wavelength=wavelength)
    q_factor = ring.calculate_q_factor(
        propagation_loss_dB_per_cm=2.0,
        coupling_coefficient=0.1
    )
    
    print(f"Operating wavelength: {wavelength} µm")
    print(f"Effective index: {effective_index}")
    print(f"Free Spectral Range (FSR): {fsr:.4f} µm ({fsr*1000:.2f} nm)")
    print(f"Quality factor (Q): {q_factor:.0f}")
    print()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
