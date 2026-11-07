import pandas as pd
import tifffile
import matplotlib.pyplot as plt

images = tifffile.imread("data/synthetic/synthetic_ld_timelapse.tif")

spots = pd.read_csv("data/synthetic/synthetic_trackmate_spots.csv", skiprows=[1, 2, 3])


frames_0_spots = spots[spots["FRAME"]==20]

print(spots.columns)

pixel_size = 0.085 #µm/pixel

x_pizels = frames_0_spots["POSITION_X"] / pixel_size
y_pixels = frames_0_spots["POSITION_Y"] / pixel_size

plt.imshow(images[20], cmap = 'gray')
plt.scatter(x_pizels, y_pixels, c='r', s=10)
plt.title(f"Frame 20 with {len(frames_0_spots)} spots")
plt.show()