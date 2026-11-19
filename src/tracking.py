import tifffile 
import numpy as np
import pandas as pd
import trackpy as tp
import matplotlib.pyplot as plt

from pathlib import Path
from skimage import feature

# Load the movie
images = tifffile.imread("data/synthetic/synthetic_ld_timelapse.tif")

def detect_spots(images):
    detections=[]
    for frame_number, frame in enumerate(images):
        # Normalize image 0-1
        frame_float = frame.astype(float)
        frame_normalized = (frame_float-frame_float.min())/(frame_float.max()-frame_float.min())

        # Detect spots
        blobs = feature.blob_log(frame_normalized, min_sigma=1, max_sigma=5, num_sigma=10, threshold=0.1)

        # Store the detections
        for y, x, sigma in blobs:
            detections.append({"frame": frame_number, "x": x, "y": y, "sigma": sigma})
    # Convert detections to pandas Dataframe 
    detections_df = pd.DataFrame(detections, columns=["frame", "x", "y", "sigma"])
    print("Total detections:", len(detections_df))
    print(detections_df.head())
    return detections_df

def link_traj(detections_df):
    # Link detected spots across frames
    tracks = tp.link_df(detections_df, search_range=5, memory=5)
    print(tracks.head())
    return tracks

# Run the analysis
detections_df = detect_spots(images)
tracks = link_traj(detections_df)

# Save the results
output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

detections_df.to_csv(output_dir / "python_detections.csv", index=False)
tracks.to_csv(output_dir / "python_tracks.csv", index=False)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(images[0], cmap="gray")
tp.plot_traj(tracks, ax=ax,label=False)
ax.set_title("Lipid droplet trajectories")
plt.show()

# Check unique trajectories
print("Total unique trajectories:", tracks["particle"].nunique())

# Check trajectory length
track_length = tracks.groupby("particle").size()
print(track_length)

track_summary=tracks.groupby("particle")["frame"].agg(["min", "max","count"])
print(track_summary)

# Checking particle 7 and 12 spatially
fig, ax = plt.subplots(4, 5, figsize=(15,12))
ax = ax.flatten()

for i, frame_number in enumerate(range(16,36)):
    # Display the corresponding image in axes[i]
    ax[i].imshow(images[frame_number], cmap="gray")
    # Set the title to the frame number
    ax[i].set_title(f'Frame={frame_number}')
    # Zoom into x= 40-75 and y= 85-115
    ax[i].set_xlim(40, 75)
    ax[i].set_ylim(85, 115)
plt.tight_layout()
plt.show()

# Filter tracks by length
tracks_length = tracks.groupby("particle").size()

long_tracks = tracks_length[tracks_length>=20]
tracks_filtered = tracks[tracks["particle"].isin(long_tracks.index)]
print(tracks_filtered)

# MSD analysis of individual spots

individual_msd = tp.imsd(tracks_filtered, mpp=0.085, max_lagtime=10, fps=2)

fig, ax = plt.subplots()
ax.plot(individual_msd.index, individual_msd, 'k-', alpha=1)  # black lines, semitransparent
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Lag time (s)")
ax.set_ylabel("MSD (µm²)")

plt.show()

# Power law fit
fit_results =[]

for particle in individual_msd:
    # Select this particle's MSD curve and remove missing values
    particle_msd = individual_msd[particle].dropna()
    # Fit the power law
    fit_imsd = tp.utils.fit_powerlaw(particle_msd, plot=False)
    # Extract fitted parameters
    alpha = fit_imsd["n"].iloc[0]
    A = fit_imsd["A"].iloc[0]
    # Store fit values
    fit_results.append({"particle":particle, "alpha": alpha, "A": A })

# Convert fit_results to pandas Dataframe 
fit_results_df = pd.DataFrame(fit_results)
print("Total fitted trajectories:", len(fit_results_df))
print(fit_results_df.head())
print("Mean individual alpha:", fit_results_df["alpha"].mean())
print(fit_results_df["alpha"].describe())

# Ensemble MSD analysis

emsd = tp.emsd(tracks_filtered, mpp=0.085, max_lagtime=10, fps=2)
fig, ax = plt.subplots()
ax.plot(emsd.index, emsd, 'k-', alpha=0.1)  # black lines, semitransparent
ax.set_xscale('log')
ax.set_yscale('log')
fit_emsd = tp.utils.fit_powerlaw(emsd)
print(f"Fit to ensemble msd:{fit_emsd}")
plt.show()

fig.savefig(
    "results/figures/trajectories.png",
    dpi=300,
    bbox_inches="tight"
)
fig.savefig(
    "results/figures/individual_msd.png",
    dpi=300,
    bbox_inches="tight"
)
fig.savefig(
    "results/figures/ensemble_msd.png",
    dpi=300,
    bbox_inches="tight"
)