import sys
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models
from cellpose import io
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

# open image data and convert to Python from Java
data = io.imread('cell_images/chosen_image.tiff')
# run Cellpose on cytoplasm (grayscale)
model = models.CellposeModel(gpu=False, model_type='cyto2')
ch = [0, 0]
cyto_labels = model.eval(data, channels=ch, diameter=30)
unique_labels = np.unique(cyto_labels[0])
num_cells = len(unique_labels[unique_labels > 0])  # Exclude label 0

mask_image = cyto_labels[0]

# Normalize to the mask's actual range for better contrast
vmin, vmax = mask_image.min(), mask_image.max()
if vmax - vmin > 0:  # Avoid division by zero
    normalized_mask = (mask_image - vmin) / (vmax - vmin)
else:
    normalized_mask = mask_image  # If uniform, keep as is
# Apply a colormap using matplotlib
cmap = plt.get_cmap('viridis')
colored_mask = cmap(normalized_mask)  # Apply colormap (RGBA output)
# Convert RGBA to RGB (drop the alpha channel)
colored_mask = (colored_mask[:, :, :3] * 255).astype(np.uint8)
mask_pil = Image.fromarray(colored_mask)
# Save the mask as a PNG file
mask_pil.save('output/output_mask.png')

# Save to a text file
with open("output/cell_number.txt", "w") as file:  # "w" mode overwrites the file if it exists
    file.write(str(num_cells))


