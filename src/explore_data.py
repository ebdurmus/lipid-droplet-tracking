import tifffile
import matplotlib.pyplot as plt

images = tifffile.imread("data/synthetic/synthetic_ld_timelapse.tif")

print("Image shape:", images.shape)
print("Data type:", images.dtype)
print("Number of frames:", images.shape[0])

fig, ax = plt.subplots(1, 2, figsize=(5, 5))
ax[0].imshow(images[0], cmap = 'gray')
ax[1].imshow(images[1], cmap = 'gray')
plt.show()
