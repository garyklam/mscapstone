# Mushroom Image Identifier

Web application that helps identify mushrooms using a Convolutional Neural Network(CNN).

## Description

The application makes an initial prediction using a CNN based on input images. The five most likley species are returned to the user along with detailed physical descriptions. Additional info about each species including toxicity, culinary usage, habitat, odor, and spore print are also provided. 
After displaying possible matches, the user can input the physical features of their specimen and compare those features to the known features of the predicted species to aid in making a positive identification. 
Additional pages provide supplementary info about mushroom physiology, how to use the identifier, and practice with identifying specific mushroom features. 

## Getting Started

### Dependencies

The app runs on an Ubunto micro EC2 instance using Python. The docker files list all required libraries, which include: Nginx, Flask, GUnicorn, pytorch-torchvision, and efficientnet-pytorch. 

### Installing
The web app is currently running on an EC2 instance at the following url: http://ec2-3-142-197-203.us-east-2.compute.amazonaws.com/ <br/>
It's possible to run the app locally, but it wasn't designed to do so. Unexpected issues may occur. 

## Authors

Gary Lam

## Version History

* 0.1
    * Initial Release

## Acknowledgements
Training data for the CNN came from the following sources:  <br/>
https://www.kaggle.com/datasets/vegameta23/mushrooms-specified  <br/>
https://github.com/visipedia/fgvcx_fungi_comp#data
