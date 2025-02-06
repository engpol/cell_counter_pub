# Cell Counter Repo
This is a public repo for running cellpose segmentation on images taken by the OpenFlexure based cell counter. 

Basic process is as follows: 

Code from OpenFlexure uploads tiled .tif image into repo.

This triggers a github action to run the segmentation script.

One action is finished, the process is detected by the microscope, which causes it to download the mask image and the .txt file holding the number of cells.

## Notes

To optimise speed as much as possible, the env is saved as a custom package in the repo itself. This is built from a docker image saved on my dockerhub profile. 
