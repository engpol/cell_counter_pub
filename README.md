# Cell Counter Repo
This is a public repo for running cellpose segmentation on images taken by the OpenFlexure-based cell counter. 

Basic process is as follows: 

30µL of cell suspension is pipetted onto a 22x22mm coverslip, and covered with a second 22x22mm coverslip. 

Code from OpenFlexure cell counter focuses on cells, takes 4 brightfield images, and uploads the tiled .tif image into repo.

This triggers a github action to run the segmentation script. This involves setting up the docker image, running cellpose cyto2 model on the tiled .tif image. The number of cells and image mask for visually inspecting segmentation serve as the output.

One action is finished, the process is detected by the microscope, which causes it to download the mask image and the .txt file holding the number of cells. This is used in the GUI for displaying your segmentation and in the calculator for performing desired dilutions.

## Tutorial

To build and use this cell counter for your research group first and foremost you will need to build the OpenFlexure cell counter with Basic Optics. The tutorial for building the microscope can be found [here](https://openflexure.org/projects/microscope/build). It will require access to at least a moderately capable 3D printer, and purchase of certain optical/mmechanical components. I have printed a functional microscope on a very chearp toy printer (Anycubic Kobra Neo 2 ~£150), however it had numerous stringing issues which may have caused slight issues with the motorized stage. If you are based in the UK/EU, you can buy all non 3D printed parts from [TauLabs](https://taulab.eu/). If you would like to buy either complete OpenFlexure kits, or even a fully assembled scope, you can find a list of vendors [here](https://openflexure.org/about/vendors). However, please keep in mind you will also need to print out the custom stage coverslip holders, found in this repo in the "stl" folder.

## Notes

To optimise speed as much as possible, the env is saved as a custom package in the repo itself. This is built from a docker image saved on my dockerhub profile. 
