import os
import requests

orthanc_url = "http://localhost:8042/instances"

authentication = ('orthanc', 'orthanc')

# Path to the directory with the DICOM files
dicom_folder = "dicom_samples"

# Iterate over the DICOM files in the folder and upload them to Orthanc
for dicom_file in os.listdir(dicom_folder):
    dicom_path = os.path.join(dicom_folder, dicom_file)
    with open(dicom_path, 'rb') as f:
        response = requests.post(orthanc_url, files={'file': f}, auth=authentication)
        print(f"Sent {dicom_file}: {response.status_code}")
