import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chaoslab.fractal import flip_time_map
from chaoslab.physics import DoublePendulumParams

def main():
    print("Generating fractal zoom frames...")
    frames = 20
    resolution = 120
    t_max = 24.0
    
    # Target center (Pretzel island)
    target_th1 = np.radians(92.0)
    target_th2 = np.radians(-96.0)
    
    # Initial bounds
    w0 = np.pi * 2
    
    # Final bounds width
    w_final = 0.5
    
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    fig.patch.set_facecolor('#12131c')
    ax.set_facecolor('#12131c')
    ax.axis('off')
    
    # We will store the images here
    ims = []
    
    params = DoublePendulumParams()
    
    for i in range(frames):
        print(f"Rendering frame {i+1}/{frames}...")
        progress = i / (frames - 1)
        # Exponential zoom
        w = w0 * (w_final / w0) ** progress
        
        # Current bounds
        th1_bounds = (target_th1 - w/2, target_th1 + w/2)
        th2_bounds = (target_th2 - w/2, target_th2 + w/2)
        
        th1, th2, flip_times = flip_time_map(
            resolution=resolution,
            t_max=t_max,
            dt=0.03,
            params=params,
            theta1_bounds=th1_bounds,
            theta2_bounds=th2_bounds
        )
        
        # Colors: map t_max to darkest, others to cmap
        # We can use a custom colormap or just plasma/inferno. Let's use inferno.
        im = ax.imshow(
            flip_times, 
            extent=[th1_bounds[0], th1_bounds[1], th2_bounds[0], th2_bounds[1]],
            origin='lower',
            cmap='inferno',
            vmin=0, vmax=t_max,
            animated=True
        )
        ims.append([im])
    
    print("Saving GIF...")
    ani = animation.ArtistAnimation(fig, ims, interval=150, blit=True, repeat_delay=1000)
    out_dir = ROOT / "presentation" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    ani.save(out_dir / "fractal_zoom.gif", writer='pillow')
    print("Done! Saved to presentation/assets/fractal_zoom.gif")

if __name__ == "__main__":
    main()
