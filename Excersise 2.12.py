import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Wedge
import matplotlib.gridspec as gridspec

# Physic constants
h = 6.626e-34         # Planck constant (J·s)
ħ = h / (2 * np.pi)   # h bar
e = 1.602e-19         # Electron charge (C)
ε0 = 8.854e-12        # Vacuum permitivity (C²/N·m²)
me = 9.109e-31        # Electron mass (kg)
a0 = 5.292e-11        # Bohr Radius (m)

class BohrAtomSimulator:
    def __init__(self):
        self.n = 1  # Fundamental state
        # Velocity for reference
        self.v_correct = e**2 / (2 * ε0 * h * self.n)
        self.calculate_properties(self.v_correct * 0.6)  # Intitializing with some value
    
    def calculate_properties(self, custom_v):
        # Orbital velocity
        self.v = custom_v
        
        # Orbital radius (fixed for comparation)
        self.r = (ε0 * h**2 * self.n**2) / (np.pi * me * e**2)
        
        # De Broglie wavelength
        self.lambda_db = h / (me * self.v)
        
        # Orbital circumference
        self.circumference = 2 * np.pi * self.r
        
        #     Number of wavelengths around the circumference
        self.n_waves = self.circumference / self.lambda_db
        
        # Energy
        self.energy = - (me * e**4) / (8 * ε0**2 * h**2 * self.n**2)
    
    def create_comparison_animation(self):
        fig = plt.figure(figsize=(14, 10))
        gs = gridspec.GridSpec(2, 2, figure=fig)  
        
        
        # First case: HIGHER speed (too many waves)
        ax1 = fig.add_subplot(gs[0, 0])
        v_high = self.v_correct * 1.8  
        self.calculate_properties(v_high)
        self.draw_atom_view(ax1, "Case A: Speed Too High\nλ too short, does not fit correctly")
        
        # Case 2: LOWER speed (incomplete waves)
        ax2 = fig.add_subplot(gs[0, 1])
        v_low = self.v_correct * 0.6 
        self.calculate_properties(v_low)
        self.draw_atom_view(ax2, "Case B: Speed Too Low\nλ too long, extra space")
        
        # Comparation
        ax3 = fig.add_subplot(gs[1, :])
        self.create_comparison_chart(ax3)
        
        plt.tight_layout()
        
        # Explanation
        self.show_explanation()
        
        plt.show()
    
    def draw_atom_view(self, ax, title):
        ax.clear()
        ax.set_xlim(-1.5 * self.r, 1.5 * self.r)
        ax.set_ylim(-1.5 * self.r, 1.5 * self.r)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=11, pad=10)
        
        # Draw nucleus
        nucleus = Circle((0, 0), self.r/10, color='red', alpha=0.8)
        ax.add_patch(nucleus)
        
        # Draw orbit
        orbit = Circle((0, 0), self.r, fill=False, color='blue', linestyle='-', alpha=0.7, linewidth=2)
        ax.add_patch(orbit)
        
        # Draw De Broglie wave around the orbit
        self.draw_de_broglie_wave(ax)
        
        # Information
        info_text = f"""
        v = {self.v:.2e} m/s
        λ = {self.lambda_db:.2e} m
        C = {self.circumference:.2e} m
        Ondas en órbita: {self.n_waves:.2f}
        """
        ax.text(1.6*self.r, 0, info_text, va='center', fontsize=9,
               bbox=dict(facecolor='white', alpha=0.8))
        
        ax.set_xticks([])
        ax.set_yticks([])
    
    def draw_de_broglie_wave(self, ax):
        """Draw the de Broglie wave around the orbit."""
        n_points = 200
        theta = np.linspace(0, 2*np.pi, n_points)
        
        # Coordenates of the orbit
        x_orbit = self.r * np.cos(theta)
        y_orbit = self.r * np.sin(theta)
        
        # Wave patern
        wave_pattern = 0.1 * self.r * np.sin(self.n_waves * theta)
        
        # Wave coordenates
        x_wave = (self.r + wave_pattern) * np.cos(theta)
        y_wave = (self.r + wave_pattern) * np.sin(theta)
        
        # Draw wave
        ax.plot(x_wave, y_wave, 'green', linewidth=2, alpha=0.8, label='De Broglie wave')
        
        # Nodes 
        node_angles = np.linspace(0, 2*np.pi, int(abs(self.n_waves)) + 1)
        for angle in node_angles:
            x_node = self.r * np.cos(angle)
            y_node = self.r * np.sin(angle)
            ax.plot(x_node, y_node, 'ro', markersize=4, alpha=0.7)
    
    def create_comparison_chart(self, ax):
        """Create a comparative graph of the two situations."""
        velocities = [
            self.v_correct * 0.6,      
            self.v_correct * 1.8       
        ]
        
        cases = ["Lower velocity", "Higher velocity"]
        n_waves_list = []
        lambda_list = []
        
        for v in velocities:
            lambda_db = h / (me * v)
            n_waves = (2 * np.pi * self.r) / lambda_db
            n_waves_list.append(n_waves)
            lambda_list.append(lambda_db)
        
        # Grafic
        x_pos = np.arange(len(cases))
        bars = ax.bar(x_pos, n_waves_list, color=['orange', 'red'], alpha=0.7)
        
        # Line
        ax.axhline(y=1.0, color='blue', linestyle='--', alpha=0.7, linewidth=2, 
                  label='Estability condition')
        
        ax.set_xlabel('Type of Speed')
        ax.set_ylabel('Number of wavelengths in the orbit')
        ax.set_title('Relationship between orbital speed and number of waves')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(cases)
        ax.legend()
        
        # Values
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   f'{n_waves_list[i]:.2f} ondas',
                   ha='center', va='bottom', fontsize=11, weight='bold')
    
   def show_explanation(self):
        """Displays physical explanation without revealing the answer"""
        print("="*80)
        print("ANALYSIS OF ORBITAL STABILITY IN THE HYDROGEN ATOM")
        print("="*80)
        print("\nOBSERVATIONS FROM THE CASES SHOWN:")
        
        print("\nCASE A - SPEED TOO HIGH:")
        print("   • The de Broglie wavelength is too short")
        print("   • Too many oscillations in the orbital circumference") 
        print("   • A coherent standing wave pattern does not form")
        
        print("\nCASE B - SPEED TOO LOW:")
        print("   • The de Broglie wavelength is too long")  
        print("   • The wave does not complete the orbital circumference")
        print("   • Complete constructive interference is lacking")
        
        print("\n" + "="*80)
        print("QUESTION FOR ANALYSIS:")
        print("What condition must the orbital speed meet so that")
        print("the electron's de Broglie wave forms a stable and")
        print("complete pattern around the nucleus?")
        print("")
        print("CONSIDER:")
        print("- The relationship between wavelength and speed")
        print("- The need for constructive interference") 
        print("- The quantization of stationary states")
        print("="*80)

# Run the comparative simulation
print("Simulating unstable orbital conditions...")
simulator = BohrAtomSimulator()
simulator.create_comparison_animation()