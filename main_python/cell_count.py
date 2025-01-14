import sys
import numpy as np
import matplotlib.pyplot as plt
import base64
from cellpose import models
from cellpose import io
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from github import Github

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


# Save to a text file
with open("output/cell_number.txt", "w") as file:  # "w" mode overwrites the file if it exists
    file.write(str(num_cells))


# GitHub Configuration
GITHUB_TOKEN = "${{ secrets.PATOKEN }}"  # Store this as a secret in GitHub Actions
REPO_OWNER = "engpol"
REPO_NAME = "Cell_Counter_Pub"
BRANCH = "main"

# Initialize GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

def upload_file_to_repo(local_file_path, repo_file_path, commit_message):
    """Uploads a local file to the GitHub repository."""
    with open(local_file_path, "rb") as f:
        content = f.read()  # Read raw binary content (no Base64 encoding)

    try:
        # Check if the file already exists
        file = repo.get_contents(repo_file_path, ref=BRANCH)
        # Update the file if it exists
        repo.update_file(
            path=file.path,
            message=commit_message,
            content=content,  # Pass raw content
            sha=file.sha,
            branch=BRANCH,
        )
        print(f"Updated file in repo: {repo_file_path}")
    except Exception as e:
        # Create the file if it doesn't exist
        repo.create_file(
            path=repo_file_path,
            message=commit_message,
            content=content,  # Pass raw content
            branch=BRANCH,
        )
        print(f"Created file in repo: {repo_file_path}")

# Push the generated files to the repo
upload_file_to_repo("output/cell_number.txt", "output/cell_number.txt", "Add cell number text file")
upload_file_to_repo("output/output_mask.png", "output/output_mask.png", "Add cell mask image")


