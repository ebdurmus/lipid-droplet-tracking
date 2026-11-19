import pandas as pd
from scipy.spatial.distance import cdist



detections_df = pd.read_csv("results/python_detections.csv")
synthetic_spots_df = pd.read_csv("data/synthetic/synthetic_trackmate_spots.csv", skiprows=[1, 2, 3])

count_detections = detections_df.groupby("frame").size()
count_synthetic_spots = synthetic_spots_df.groupby("FRAME").size()

print(count_detections)
print(count_synthetic_spots)


comparison_df = pd.DataFrame({
    "LoG": count_detections,
    "Reference": count_synthetic_spots,
    "Difference": count_detections - count_synthetic_spots
})

print(comparison_df.head())
print(comparison_df["Difference"].describe())

comparison_df.index.name = "frame"
comparison_df.to_csv("results/detection_comparison.csv", index=True)

log_frame0 = detections_df[detections_df["frame"]==0]
ref_frame0 = synthetic_spots_df[synthetic_spots_df["FRAME"]==0]
ref_frame0 = ref_frame0.copy()

pixel_size = 0.085 #µm/pixel

ref_frame0["x_pixels"] = ref_frame0["POSITION_X"] / pixel_size
ref_frame0["y_pixels"] = ref_frame0["POSITION_Y"] / pixel_size

ref_frame0 = ref_frame0.copy()

print(log_frame0[["x", "y"]].head())
print(ref_frame0[["x_pixels", "y_pixels"]].head())

print("LoG detections:", len(log_frame0))
print("Reference detections:", len(ref_frame0))

log_coords = log_frame0[["x", 'y']].to_numpy()
ref_coords = ref_frame0[["x_pixels", "y_pixels"]].to_numpy()

print(log_coords.shape)
print(ref_coords.shape)

distance_matrix = cdist(log_coords, ref_coords)

print(distance_matrix.shape)
print(distance_matrix.round(2))

distance_matrix[0]
print(distance_matrix[0].min())

print(distance_matrix[0].argmin())

closest_refs = distance_matrix.argmin(axis=1)
print(closest_refs)