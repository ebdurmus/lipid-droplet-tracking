# Lipid Droplet Tracking and Mobility Analysis


A Python-based workflow for detecting and tracking lipid droplets in synthetic time-lapse fluorescence microscopy images, followed by quantitative analysis of their mobility using mean-squared displacement (MSD).
Analysis Workflow
1. Spot Detection
- Load time-lapse TIFF images using tifffile.
- Normalize image intensity.
- Detect fluorescent spots using the Laplacian of Gaussian (LoG) algorithm from scikit-image.
2. Trajectory Reconstruction
- Link detections across frames using trackpy.
- Allow temporary detection gaps using the tracking memory parameter.
- Export detected spots and reconstructed trajectories as CSV files.
3. Motion Analysis
- Filter trajectories by minimum detection count.
- Calculate individual and ensemble MSD curves.
- Fit the power-law model:
$$
MSD(\tau) = A\tau^\alpha
$$

- Extract the anomalous diffusion exponent (α) and power-law prefactor (A) for individual trajectories.
4. Preliminary Validation
- Compare LoG detection counts with a supplied synthetic reference dataset across 60 frames.
- Examine spatial agreement between detections and reference positions in a representative frame.
Methods and Parameters
Parameter	Value
Image dimensions	128 × 128 pixels
Number of frames	60
Pixel size	0.085 µm/pixel
Frame interval	0.5 s
Detection algorithm	Laplacian of Gaussian (LoG)
LoG sigma range	1–5 pixels
LoG threshold	0.1
Tracking search range	5 pixels
Tracking memory	5 frames
Minimum trajectory length	20 detections
Maximum MSD lag time	10 frames (5 s)

Example Results
The pipeline reconstructs particle trajectories from synthetic fluorescence images and generates individual and ensemble MSD curves.
Reconstructed Trajectories
Individual MSD
Ensemble MSD
Preliminary Quantitative Results
Measurement	Result
Trajectories retained after filtering	11
Mean individual anomalous exponent (α)	0.907
Ensemble anomalous exponent (α)	0.948
Mean difference in detections per frame (LoG − reference)	+0.45

These results are exploratory and should not be interpreted as evidence of distinct biological motion populations.
Limitations
The pipeline is currently demonstrated using synthetic data. Particle overlap, missing detections, and ambiguous trajectory linking can affect reconstruction accuracy.

Validation is preliminary and does not yet constitute a comprehensive benchmark against known particle identities. Differences in detection counts do not establish detection accuracy.

MSD power-law estimates may be influenced by finite trajectory length, localization uncertainty, and the selected fitting interval.
Installation
Clone the repository and install the dependencies:
Installation
Clone the repository and install the dependencies:
git clone https://github.com/ebdurmus/lipid-droplet-tracking.git
cd lipid-droplet-tracking

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


Usage
Run the scripts from the repository's root directory.

1. Detection and tracking
python src/tracking.py


Generates the detected spots and reconstructed trajectories.

2. MSD analysis
python src/msd_analysis.py


Calculates individual and ensemble MSD curves and fits power-law models.

3. Preliminary validation
python src/validation.py


Compares detection counts with the synthetic reference dataset.

Analysis outputs are saved in the results/ directory.
Technologies
Python · NumPy · pandas · SciPy · scikit-image · trackpy · Matplotlib · tifffile
</CodeBlock>