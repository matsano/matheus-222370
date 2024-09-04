import torchxrayvision as xrv
from torchvision import transforms
import torch
import os
from read_xray_dicom import read_xray_dcm
import json

def classify_dicom_image(image):
    # To perform future transformations, the image must have a channel dimension, so the channel dimension (grayscale) is added
    image = image[None, ...]

    # Define and apply a series of transformations (crop the image around the center to get the most centered part
    # and resize the image to 224x224, which is the input size of DenseNet)
    transform = transforms.Compose([
        xrv.datasets.XRayCenterCrop(),
        xrv.datasets.XRayResizer(224)
    ])
    
    image_transformed = transform(image)

    # Transform the image into a tensor and add a dimension that corresponds to the batch_size (only 1 image in the batch)
    image_tensor = torch.from_numpy(image_transformed)
    image_tensor = image_tensor[None, ...]

    # Get predictions from a DesNet
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    model.eval()
    with torch.no_grad():
        outputs = model(image_tensor)

    # Obtain the possible pathologies and their probabilities estimated by the model
    pathologies = model.pathologies
    probs_pathologies = outputs[0].detach().numpy()
    
    return dict(zip(pathologies, probs_pathologies.tolist()))


if __name__ == "__main__":
    
    directory_images = 'dicom_samples'
    for file in os.listdir(directory_images):
        
        # Loads the DICOM file and stores it in a 2D numpy
        image = read_xray_dcm(os.path.join(directory_images, file))
        
        # Execute classification with DenseNet
        result = classify_dicom_image(image)
        
        # Save predictions to a JSON file
        result_file = 'results_classification/' + os.path.splitext(file)[0] + '.json'
        with open(result_file, 'w') as json_file:
            json.dump(result, json_file)
