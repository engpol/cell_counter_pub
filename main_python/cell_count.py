import sys
import numpy as np
import matplotlib.pyplot as plt
import base64
from cellpose import models
from cellpose import io
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

encoded_file_path = "cell_images/chosen_image.tiff"  # File containing Base64-encoded tiff image
decoded_file_path = "cell_images/decoded_image.tiff" # File with decoded tiff image

with open(encoded_file_path, "r") as encoded_file: # Read tiff image
    encoded_content = encoded_file.read()
    
# Step 2: Decode the Base64 content
decoded_content = base64.b64decode(encoded_content)

# Step 3: Write the decoded binary data back to a TIFF file
with open(decoded_file_path, "wb") as decoded_file:
    decoded_file.write(decoded_content)

# open image data and convert to Python from Java
data = io.imread('cell_images/decoded_image.tiff')
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


