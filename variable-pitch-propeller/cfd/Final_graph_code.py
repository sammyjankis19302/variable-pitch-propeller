import math
import numpy as np

# Constants
rho = 1.225  # Air density (kg/m³)
diameter = 0.328  # Propeller diameter in meters (328mm)
radius = diameter / 2
area = math.pi * radius**2  # Propeller disk area (m²)

print(f"Propeller Parameters:")
print(f"Diameter: {diameter*1000:.0f} mm")
print(f"Area: {area:.6f} m²")
print(f"Air density (ρ): {rho} kg/m³")
print("-" * 50)

# Predefined data for 5 different pitch angles with their corresponding vin, vout, and mass flow rate values
propeller_data = [
    {"pitch_angle": 0, "vin": 5.44117, "vout": 6.78951, "mass_flow_rate": 0.5188},
    {"pitch_angle": 2, "vin": 8.17492, "vout": 7.67, "mass_flow_rate": 0.5668},
    {"pitch_angle": 4, "vin": 6.534, "vout": 8.389, "mass_flow_rate": 0.414},
    {"pitch_angle": 6, "vin": 8.7986, "vout": 10.479, "mass_flow_rate": 0.7939},
    {"pitch_angle": 8, "vin": 7.624, "vout": 6.384, "mass_flow_rate": 0.589},
    {"pitch_angle": 10, "vin": 7.111, "vout": 5.456, "mass_flow_rate": 0.519},
    {"pitch_angle": 12, "vin": 6.234, "vout": 9.468, "mass_flow_rate": 0.6267},
    {"pitch_angle": 14, "vin": 6.976, "vout": 6.404, "mass_flow_rate": 0.7207},
    {"pitch_angle": 16, "vin": 5.1807, "vout": 8.99506, "mass_flow_rate": 0.590481},
    {"pitch_angle": 18, "vin": 6.552, "vout": 3.331, "mass_flow_rate": 0.6663},
    {"pitch_angle": 20, "vin": 10.1062, "vout":9.58229 , "mass_flow_rate": 1.16587},
    {"pitch_angle": 21, "vin": 3.24958, "vout": 88.66462, "mass_flow_rate": 0.334198},
    {"pitch_angle": 22, "vin": 8.874, "vout": 11.001, "mass_flow_rate": 0.9582},
    {"pitch_angle": 24, "vin": 8.425, "vout": 10.712, "mass_flow_rate": 0.8903},
    {"pitch_angle": 26, "vin": 9.045, "vout": 12.235, "mass_flow_rate": 1.0201},
    {"pitch_angle": 28, "vin": 8.814, "vout": 11.444, "mass_flow_rate": 0.9612},
    {"pitch_angle": 30, "vin": 9.588, "vout": 11.788, "mass_flow_rate": 0.9803}

]

def calculate_thrust(vin, vout):
    """
    Calculate thrust using the formula: ρ × A × vavg × (vout - vin)
    """
    # Average velocity
    vavg = (vin + vout) / 2
    
    # Thrust calculation using given formula
    thrust = rho * area * vavg * (vout - vin)
    
    return thrust, vavg

print("Thrust Calculations:")
print(f"{'Pitch Angle (°)':<15} {'vin (m/s)':<12} {'vout (m/s)':<12} {'Mass Flow (kg/s)':<15} {'vavg (m/s)':<12} {'Thrust (N)':<12}")
print("-" * 95)

results = []
for data in propeller_data:
    angle = data["pitch_angle"]
    vin = data["vin"]
    vout = data["vout"]
    mass_flow = data["mass_flow_rate"]
    thrust, vavg = calculate_thrust(vin, vout)
    results.append((angle, thrust, vin, vout, vavg, mass_flow))
    print(f"{angle:<15} {vin:<12.2f} {vout:<12.2f} {mass_flow:<15.2f} {vavg:<12.2f} {thrust:<12.2f}")

print("-" * 95)
print(f"Maximum thrust: {max(results, key=lambda x: x[1])[1]:.2f} N at {max(results, key=lambda x: x[1])[0]}°")
print(f"Minimum thrust: {min(results, key=lambda x: x[1])[1]:.2f} N at {min(results, key=lambda x: x[1])[0]}°")

# Extract data for plotting
angles = [r[0] for r in results]
thrusts = [r[1] for r in results]
vins = [r[2] for r in results]
vouts = [r[3] for r in results]
vavgs = [r[4] for r in results]
mass_flows = [r[5] for r in results]

# Calculate additional parameters
velocity_differences = [vout - vin for vin, vout in zip(vins, vouts)]
thrust_to_mass_ratio = [thrust/mass_flow for thrust, mass_flow in zip(thrusts, mass_flows)]

# Plotting
try:
    import matplotlib.pyplot as plt
    
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Propeller Performance Analysis', fontsize=18, fontweight='bold', y=0.98)
    
    # Plot 1: Pitch Angle vs Thrust
    axes[0, 0].plot(angles, thrusts, 'b-o', linewidth=2, markersize=8)
    axes[0, 0].set_xlabel('Pitch Angle (°)', fontsize=10)
    axes[0, 0].set_ylabel('Thrust (N)', fontsize=10)
    axes[0, 0].set_title('Pitch Angle vs Thrust', fontsize=12, pad=15)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='both', which='major', labelsize=9)
    
    # Plot 2: Pitch Angle vs Mass Flow Rate
    axes[0, 1].plot(angles, mass_flows, 'r-s', linewidth=2, markersize=8)
    axes[0, 1].set_xlabel('Pitch Angle (°)', fontsize=10)
    axes[0, 1].set_ylabel('Mass Flow Rate (kg/s)', fontsize=10)
    axes[0, 1].set_title('Pitch Angle vs Mass Flow Rate', fontsize=12, pad=15)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(axis='both', which='major', labelsize=9)
    
    # Plot 3: Mass Flow Rate vs Thrust
    axes[0, 2].plot(mass_flows, thrusts, 'g-^', linewidth=2, markersize=8)
    axes[0, 2].set_xlabel('Mass Flow Rate (kg/s)', fontsize=10)
    axes[0, 2].set_ylabel('Thrust (N)', fontsize=10)
    axes[0, 2].set_title('Mass Flow Rate vs Thrust', fontsize=12, pad=15)
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].tick_params(axis='both', which='major', labelsize=9)
    
    # Plot 4: Pitch Angle vs Velocity Difference (vout - vin)
    axes[1, 0].plot(angles, velocity_differences, 'm-d', linewidth=2, markersize=8)
    axes[1, 0].set_xlabel('Pitch Angle (°)', fontsize=10)
    axes[1, 0].set_ylabel('Velocity Difference (m/s)', fontsize=10)
    axes[1, 0].set_title('Pitch Angle vs Velocity Difference', fontsize=12, pad=15)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='both', which='major', labelsize=9)
    
    # Plot 5: Average Velocity vs Thrust
    axes[1, 1].plot(vavgs, thrusts, 'c-p', linewidth=2, markersize=8)
    axes[1, 1].set_xlabel('Average Velocity (m/s)', fontsize=10)
    axes[1, 1].set_ylabel('Thrust (N)', fontsize=10)
    axes[1, 1].set_title('Average Velocity vs Thrust', fontsize=12, pad=15)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].tick_params(axis='both', which='major', labelsize=9)
    
    # Plot 6: Thrust to Mass Flow Ratio vs Pitch Angle
    axes[1, 2].plot(angles, thrust_to_mass_ratio, 'orange', marker='h', linewidth=2, markersize=8)
    axes[1, 2].set_xlabel('Pitch Angle (°)', fontsize=10)
    axes[1, 2].set_ylabel('Thrust/Mass Flow\n(N·s/kg)', fontsize=10)
    axes[1, 2].set_title('Thrust Efficiency vs Pitch Angle', fontsize=12, pad=15)
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].tick_params(axis='both', which='major', labelsize=9)
    
    plt.tight_layout(pad=3.0, h_pad=3.0, w_pad=2.0)
    plt.subplots_adjust(top=0.92)
    plt.show()
    
    # Additional analysis plots
    fig2, axes2 = plt.subplots(1, 2, figsize=(15, 6))
    fig2.suptitle('Velocity Analysis', fontsize=16, fontweight='bold', y=0.98)
    
    # Plot: Pitch Angle vs Inlet and Outlet Velocities
    axes2[0].plot(angles, vins, 'b-o', linewidth=2, markersize=6, label='Inlet Velocity (vin)')
    axes2[0].plot(angles, vouts, 'r-s', linewidth=2, markersize=6, label='Outlet Velocity (vout)')
    axes2[0].plot(angles, vavgs, 'g-^', linewidth=2, markersize=6, label='Average Velocity (vavg)')
    axes2[0].set_xlabel('Pitch Angle (°)', fontsize=11)
    axes2[0].set_ylabel('Velocity (m/s)', fontsize=11)
    axes2[0].set_title('Velocities vs Pitch Angle', fontsize=12, pad=15)
    axes2[0].legend(fontsize=10)
    axes2[0].grid(True, alpha=0.3)
    axes2[0].tick_params(axis='both', which='major', labelsize=10)
    
    # Plot: 3D scatter plot (Mass Flow vs Thrust vs Pitch Angle)
    from mpl_toolkits.mplot3d import Axes3D
    ax3d = fig2.add_subplot(122, projection='3d')
    scatter = ax3d.scatter(mass_flows, thrusts, angles, c=angles, cmap='viridis', s=100)
    ax3d.set_xlabel('Mass Flow Rate\n(kg/s)', fontsize=10)
    ax3d.set_ylabel('Thrust (N)', fontsize=10)
    ax3d.set_zlabel('Pitch Angle (°)', fontsize=10)
    ax3d.set_title('3D: Mass Flow vs Thrust vs Pitch', fontsize=12, pad=20)
    ax3d.tick_params(axis='both', which='major', labelsize=9)
    
    # Add colorbar for 3D plot
    cbar = plt.colorbar(scatter, ax=ax3d, shrink=0.8, aspect=20)
    cbar.set_label('Pitch Angle (°)', fontsize=10)
    
    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(top=0.90)
    plt.show()
    
    # Print correlation analysis
    print("\n" + "="*50)
    print("CORRELATION ANALYSIS")
    print("="*50)
    
    correlation_thrust_mass = np.corrcoef(thrusts, mass_flows)[0,1]
    correlation_angle_thrust = np.corrcoef(angles, thrusts)[0,1]
    correlation_angle_mass = np.corrcoef(angles, mass_flows)[0,1]
    
    print(f"Correlation between Thrust and Mass Flow Rate: {correlation_thrust_mass:.3f}")
    print(f"Correlation between Pitch Angle and Thrust: {correlation_angle_thrust:.3f}")
    print(f"Correlation between Pitch Angle and Mass Flow Rate: {correlation_angle_mass:.3f}")
    
    # Find optimal pitch angle
    max_thrust_idx = thrusts.index(max(thrusts))
    max_efficiency_idx = thrust_to_mass_ratio.index(max(thrust_to_mass_ratio))
    
    print(f"\nOptimal pitch angle for maximum thrust: {angles[max_thrust_idx]}°")
    print(f"Optimal pitch angle for maximum efficiency: {angles[max_efficiency_idx]}°")
    
except ImportError:
    print("\nNote: Install matplotlib and numpy to see the plots and correlation analysis")
    print("pip install matplotlib numpy")