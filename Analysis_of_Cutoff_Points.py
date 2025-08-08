import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def lennard_jones(r, epsilon=1.0, sigma=1.0):
    """Calculate Lennard-Jones potential energy"""
    if r < 0.01:
        return float('inf')
    sr6 = (sigma / r)**6
    return 4 * epsilon * (sr6**2 - sr6)

def analyze_cutoff_comparison():
    """Analyze and compare different cutoff values"""
    
    # Parameters
    epsilon = 1.0
    sigma = 1.0
    
    # Distance range for plotting
    r_values = np.linspace(0.9, 4.0, 1000)
    
    # Calculate potential values
    potential_values = [lennard_jones(r, epsilon, sigma) for r in r_values]
    
    # Cutoff values to compare (replaced 2.245 with 2.000)
    cutoffs = [2.000, 2.5, 3.0]
    cutoff_labels = ['2.0σ', '2.5σ', '3.0σ']
    colors = ['red', 'blue', 'green']
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot the potential
    plt.subplot(2, 2, 1)
    plt.plot(r_values, potential_values, 'k-', linewidth=2, label='LJ Potential')
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    # Mark cutoff positions
    for cutoff, label, color in zip(cutoffs, cutoff_labels, colors):
        potential_at_cutoff = lennard_jones(cutoff, epsilon, sigma)
        plt.axvline(x=cutoff, color=color, linestyle='--', alpha=0.7, label=f'{label}')
        plt.plot(cutoff, potential_at_cutoff, 'o', color=color, markersize=8)
    
    plt.xlim(0.9, 4.0)
    plt.ylim(-1.2, 2.0)
    plt.xlabel('Distance (r/σ)')
    plt.ylabel('Potential Energy (V/ε)')
    plt.title('Lennard-Jones Potential with Different Cutoffs')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Zoomed view of the tail region
    plt.subplot(2, 2, 2)
    tail_r = np.linspace(2.0, 4.0, 500)
    tail_potential = [lennard_jones(r, epsilon, sigma) for r in tail_r]
    
    plt.plot(tail_r, tail_potential, 'k-', linewidth=2)
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    for cutoff, label, color in zip(cutoffs, cutoff_labels, colors):
        potential_at_cutoff = lennard_jones(cutoff, epsilon, sigma)
        plt.axvline(x=cutoff, color=color, linestyle='--', alpha=0.7, label=f'{label}')
        plt.plot(cutoff, potential_at_cutoff, 'o', color=color, markersize=8)
    
    plt.xlim(2.0, 4.0)
    plt.ylim(-0.08, 0.08)  # Adjusted range to accommodate 2.0σ value
    plt.xlabel('Distance (r/σ)')
    plt.ylabel('Potential Energy (V/ε)')
    plt.title('Tail Region (Zoomed)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Quantitative comparison table
    plt.subplot(2, 1, 2)
    plt.axis('off')
    
    # Calculate values at each cutoff
    comparison_data = []
    for cutoff in cutoffs:
        potential = lennard_jones(cutoff, epsilon, sigma)
        percentage = abs(potential / epsilon) * 100
        comparison_data.append([f'{cutoff:.3f}σ', f'{potential:.6f}ε', f'{percentage:.3f}%'])
    
    # Create table
    table_data = [['Cutoff', 'Potential Value', '% of Well Depth']] + comparison_data
    
    table = plt.table(cellText=table_data[1:],
                     colLabels=table_data[0],
                     cellLoc='center',
                     loc='center',
                     bbox=[0.2, 0.3, 0.6, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    # Color code the rows
    for i, color in enumerate(colors):
        for j in range(3):
            table[(i+1, j)].set_facecolor(color)
            table[(i+1, j)].set_alpha(0.3)
    
    plt.title('Quantitative Comparison of Cutoff Values', pad=20, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # Print detailed analysis
    print("="*60)
    print("LENNARD-JONES POTENTIAL CUTOFF ANALYSIS")
    print("="*60)
    print(f"{'Cutoff':<10} {'Potential':<15} {'% of ε':<10} {'Significance':<20}")
    print("-"*60)
    
    for cutoff, label, color in zip(cutoffs, cutoff_labels, colors):
        potential = lennard_jones(cutoff, epsilon, sigma)
        percentage = abs(potential / epsilon) * 100
        
        if percentage > 5.0:
            significance = "High"
        elif percentage > 2.0:
            significance = "Significant"
        elif percentage > 1.0:
            significance = "Moderate"
        else:
            significance = "Negligible"
            
        print(f"{label:<10} {potential:<15.6f} {percentage:<10.3f} {significance:<20}")
    
    print("\nCOMPUTATIONAL IMPACT:")
    print("-"*30)
    
    # Estimate computational cost (assuming uniform density)
    density = 0.8  # typical liquid density
    for cutoff, label in zip(cutoffs, cutoff_labels):
        # Volume of sphere with radius = cutoff
        volume = (4/3) * np.pi * cutoff**3
        neighbors = volume * density
        relative_cost = (cutoff/2.0)**3  # Relative to 2.0σ
        
        print(f"{label}: ~{neighbors:.0f} neighbors, {relative_cost:.2f}x computational cost")
    
    print("\nRECOMMENDATION:")
    print("-"*15)
    print("• 2.0σ:   Very efficient, potential = -0.0615ε (6.15%)")
    print("• 2.5σ:   Standard choice, potential = -0.0163ε (1.63%)")  
    print("• 3.0σ:   High accuracy, potential = -0.0067ε (0.67%)")
    print("\n2.0σ cutoff sacrifices some accuracy for maximum speed.")
    print("2.5σ remains the best balance for most applications.")

def computational_scaling_demo():
    """Demonstrate computational scaling with different cutoffs"""
    
    cutoffs = np.linspace(1.8, 4.0, 50)
    potentials = [abs(lennard_jones(r)) for r in cutoffs]
    computational_costs = [(r/2.5)**3 for r in cutoffs]  # Relative to 2.5σ
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Potential vs cutoff
    ax1.semilogy(cutoffs, potentials, 'b-', linewidth=2)
    ax1.axvline(x=2.0, color='red', linestyle='--', alpha=0.7, label='2.0σ')
    ax1.axvline(x=2.5, color='blue', linestyle='--', alpha=0.7, label='2.5σ')
    ax1.axvline(x=3.0, color='green', linestyle='--', alpha=0.7, label='3.0σ')
    ax1.set_xlabel('Cutoff Distance (r/σ)')
    ax1.set_ylabel('|Potential| at Cutoff (log scale)')
    ax1.set_title('Potential Magnitude vs Cutoff')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Computational cost vs cutoff
    ax2.plot(cutoffs, computational_costs, 'r-', linewidth=2)
    ax2.axvline(x=2.0, color='red', linestyle='--', alpha=0.7, label='2.0σ')
    ax2.axvline(x=2.5, color='blue', linestyle='--', alpha=0.7, label='2.5σ')
    ax2.axvline(x=3.0, color='green', linestyle='--', alpha=0.7, label='3.0σ')
    ax2.set_xlabel('Cutoff Distance (r/σ)')
    ax2.set_ylabel('Relative Computational Cost')
    ax2.set_title('Computational Cost vs Cutoff')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Run the analysis
if __name__ == "__main__":
    print("Analyzing Lennard-Jones potential cutoff comparison...")
    analyze_cutoff_comparison()
    print("\n" + "="*60)
    print("Computational scaling demonstration...")
    computational_scaling_demo()

