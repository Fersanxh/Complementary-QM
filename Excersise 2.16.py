import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Physical constants
h = 6.626e-34         # Planck constant (J·s)
ħ = h / (2 * np.pi)   # h bar (J·s)
c = 2.998e8           # Speed of light (m/s)
k = 1.381e-23         # Boltzmann constant (J/K)
eV = 1.602e-19        # 1 electronvolt in joules

def zero_point_energy(wavelength):
    """Calculates the zero-point energy for a given wavelength"""
    omega = 2 * np.pi * c / wavelength
    return 0.5 * ħ * omega

def thermal_energy(wavelength, temperature):
    """Calculates the average thermal energy for a given wavelength and temperature"""
    omega = 2 * np.pi * c / wavelength
    numerator = ħ * omega
    exponent = ħ * omega / (k * temperature)
    
    # Handle cases where exponent is very large (avoid overflow)
    # For large exponents, thermal energy is approximately 0
    thermal_energy = np.zeros_like(wavelength)
    
    # Where exponent is manageable, calculate normally
    mask = exponent < 100  # Avoid numerical overflow
    denominator = np.exp(exponent[mask]) - 1
    thermal_energy[mask] = numerator[mask] / denominator
    
    return thermal_energy

def create_comparison_plot():
    # Initial configuration
    wavelengths_nm = np.linspace(100, 10000, 500)  # 100 nm to 10000 nm
    wavelengths_m = wavelengths_nm * 1e-9
    T_room = 300  # Room temperature (K)
    
    # Calculate energies
    E0 = zero_point_energy(wavelengths_m) / eV  # Convert to eV
    E_thermal = thermal_energy(wavelengths_m, T_room) / eV  # Convert to eV
    
    # Create figure and axes - SOLO UN SUBPLOT
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))
    plt.subplots_adjust(bottom=0.15)
    
    # Plot 1: Energies vs Wavelength
    line1, = ax1.plot(wavelengths_nm, E0, 'b-', linewidth=2, label='Zero-point energy (E₀)')
    line2, = ax1.plot(wavelengths_nm, E_thermal, 'r-', linewidth=2, label='Thermal energy (300K)')
    
    # Mark 6000 Å (600 nm)
    wavelength_6000A = 600  # nm
    idx_6000 = np.abs(wavelengths_nm - wavelength_6000A).argmin()
    ax1.axvline(x=wavelength_6000A, color='green', linestyle='--', alpha=0.7, 
                label=f'6000 Å ({wavelength_6000A} nm)')
    ax1.plot(wavelength_6000A, E0[idx_6000], 'bo', markersize=8)
    ax1.plot(wavelength_6000A, E_thermal[idx_6000], 'ro', markersize=8)
    
    ax1.set_xlabel('Wavelength (nm)')
    ax1.set_ylabel('Energy (eV)')
    ax1.set_title('Comparison: Zero-point energy vs Thermal energy (300K)')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add information text
    info_text = f"""For 6000 Å (600 nm):
E₀ = {E0[idx_6000]:.3f} eV
E_thermal = {E_thermal[idx_6000]:.3e} eV
Ratio = {E_thermal[idx_6000]/E0[idx_6000]:.3e}"""
    
    ax1.text(0.02, 0.98, info_text, transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.show()


# Function for detailed calculation of the specific 6000 Å case
def calculate_specific_case():
    wavelength_6000A = 6000 * 1e-10  # 6000 Å in meters
    T_room = 300  # K
    
    # Zero-point energy
    omega = 2 * np.pi * c / wavelength_6000A
    E0 = 0.5 * ħ * omega / eV
    
    # Thermal energy
    numerator = ħ * omega
    exponent = ħ * omega / (k * T_room)
    
    if exponent > 100:  # Avoid overflow
        E_thermal = 0.0
    else:
        denominator = np.exp(exponent) - 1
        E_thermal = numerator / denominator / eV
    
    ratio = E_thermal / E0 if E0 != 0 else 0
    
    print("="*60)
    print("DETAILED CALCULATION FOR 6000 Å")
    print("="*60)
    print(f"Wavelength: {wavelength_6000A * 1e10:.1f} Å")
    print(f"Angular frequency (ω): {omega:.3e} rad/s")
    print(f"Zero-point energy (E₀): {E0:.4f} eV")
    print(f"ħω: {ħ * omega / eV:.4f} eV")
    print(f"kT (300K): {k * T_room / eV:.6f} eV")
    print(f"Exponent (ħω/kT): {exponent:.1f}")
    print(f"Thermal energy: {E_thermal:.3e} eV")
    print(f"Ratio E_thermal/E₀: {ratio:.3e}")
    print("="*60)


# Execute the program
if __name__ == "__main__":
    calculate_specific_case()
    create_comparison_plot()