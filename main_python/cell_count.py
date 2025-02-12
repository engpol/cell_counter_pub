import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import base64
import requests
from cellpose import models
from cellpose import io
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from github import Github

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is missing.")    
REPO_OWNER = "engpol"
REPO_NAME = "cell_counter_pub"
BRANCH = "main"

# Initialize GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

def download_file_from_raw_url(remote_path, local_path):
    """Downloads a file from the raw GitHub URL."""
    # Construct the raw URL
    raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{remote_path}"
    
    # Make the HTTP request
    response = requests.get(raw_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            decoded_content = base64.b64decode(response.content)
            f.write(decoded_content)  # Write the raw content to a file
        print(f"File '{remote_path}' downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

local_path = os.path.join(os.getcwd(), "decoded_image.tiff")
download_file_from_raw_url("cell_images/chosen_image.tiff", local_path)


# open image data and convert to Python from Java
data = io.imread(local_path)
# run Cellpose on cytoplasm (grayscale)
model = models.CellposeModel(gpu=False, model_type='cyto2')
ch = [0, 0]
cyto_labels = model.eval(data, channels=ch, diameter=25)
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
local_path_mask = os.path.join(os.getcwd(), "output_mask.png")
mask_pil.save(local_path_mask)
local_path_number = os.path.join(os.getcwd(), "cell_number.txt")
# Save to a text file
with open(local_path_number, "w") as file:  # "w" mode overwrites the file if it exists
    file.write(str(num_cells))

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
upload_file_to_repo(local_path_number, "output/cell_number.txt", "Add cell number text file")
upload_file_to_repo(local_path_mask, "output/output_mask.png", "Add cell mask image")


