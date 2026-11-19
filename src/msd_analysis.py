import pandas as pd
import trackpy as tp
import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

#Load the trajectories
tracks = pd.read_csv("results/python_tracks.csv")


track_summary=tracks.groupby("particle")["frame"].agg(["min", "max","count"])
print(track_summary)

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
    particle_msd = particle_msd[particle_msd > 0]
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
ax.plot(emsd.index, emsd, 'k-', alpha=1)  # black lines, semitransparent
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Lag time (s)")
ax.set_ylabel("MSD (µm²)")

fit_emsd = tp.utils.fit_powerlaw(emsd, plot= False)
print(f"Fit to ensemble msd:{fit_emsd}")
plt.show()

# Save results to CSV files
individual_msd.index.name = "lag_time_s"
emsd.index.name = "lag_time_s"

emsd.to_csv(output_dir / "ensemble_msd.csv", index=True)
individual_msd.to_csv(output_dir / "individual_msd.csv", index=True)
fit_results_df.to_csv(output_dir / "powerlaw_fits.csv", index=False)



