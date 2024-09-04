import os
import json
import requests
from pydicom import dcmread
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from pynetdicom.sop_class import EnhancedSRStorage



def create_dicom_sr(dicom_image_path, json_results_path):
    
    # Load DICOM file
    dicom_image = dcmread(dicom_image_path)
    
    # Load json file
    with open(json_results_path, 'r') as f:
        json_results = json.load(f)
    
    # Create a DICOM SR dataset
    dicom_sr = Dataset()
    
    # Configure the DICOM file metadata, identifying the type of data present in the DICOM file
    dicom_sr.file_meta = FileMetaDataset()
    dicom_sr.file_meta.MediaStorageSOPClassUID = EnhancedSRStorage
    dicom_sr.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    dicom_sr.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    
    # A SOP Class is a class that defines the type of data and the operations that can be performed on that data.
    # Therefore, you should define the SOP Class as Enhanced Structured Report
    dicom_sr.SOPClassUID = EnhancedSRStorage
    dicom_sr.SOPInstanceUID = generate_uid()
    
    # Define the content of the DICOM file as a Structured Report
    dicom_sr.Modality = "SR"
    
    # Add information identifying patient, study and series
    dicom_sr.PatientName = dicom_image.PatientName
    dicom_sr.PatientID = dicom_image.PatientID
    dicom_sr.StudyInstanceUID = dicom_image.StudyInstanceUID
    dicom_sr.SeriesInstanceUID = dicom_image.SeriesInstanceUID
    
    # Add structured report content
    dicom_sr.ContentSequence = []
    for task, probability in json_results.items():
        # Add a new Dataset object to store data related to a specific task
        item = Dataset()
        
        # Define the concept code sequence for a task
        item.ConceptNameCodeSequence = [Dataset()]
        item.ConceptNameCodeSequence[0].CodeValue = 'Task'
        item.ConceptNameCodeSequence[0].CodeMeaning = task
        
        # Define the coding system as DCM, used for codes defined specifically in the DICOM standard,
        # without the need to be represented by a standard clinical coding system
        item.ConceptNameCodeSequence[0].CodingSchemeDesignator = 'DCM'
        
        # Define the unit of measurement for the measured value
        item.MeasurementUnitsCodeSequence = [Dataset()]
        item.MeasurementUnitsCodeSequence[0].CodeValue = 'PERCENT'
        item.MeasurementUnitsCodeSequence[0].CodeMeaning = 'Percent'
        
        # The coding system is UCUM, used to represent units of measurement
        item.MeasurementUnitsCodeSequence[0].CodingSchemeDesignator = 'UCUM'
        
        # Store the probability corresponding to the task
        item.ValueType = 'NUM'
        item.NumericValue = probability * 100
        
        dicom_sr.ContentSequence.append(item)
    
    dicom_sr.DocumentTitle = "Report of the findings classification with TorchRayVision"
    
    return dicom_sr


def send_dicom_sr_to_pacs():
    
    orthanc_url = "http://localhost:8042/instances"
    authentication = ('orthanc', 'orthanc')

    # Path to the directory with the DICOM SR files
    dicom_sr_folder = "results_dicom_rs"

    # Iterate over the DICOM SR files in the folder and upload them to Orthanc
    for dicom_file in os.listdir(dicom_sr_folder):
        dicom_path = os.path.join(dicom_sr_folder, dicom_file)
        with open(dicom_path, 'rb') as f:
            response = requests.post(orthanc_url, files={'file': f}, auth=authentication)
            print(f"Sent {dicom_file}: {response.status_code}")





if __name__ == "__main__":
    
    dicom_image_dir = sorted(os.listdir('dicom_samples'))
    json_results_dir = sorted(os.listdir('results_classification'))
    
    # Create the DICOM SR file and save it
    for dicom_file, json_file in zip(dicom_image_dir, json_results_dir):
        dicom_image_path = os.path.join('dicom_samples', dicom_file)
        json_results_path = os.path.join('results_classification', json_file)
        
        dicom_sr = create_dicom_sr(dicom_image_path, json_results_path)
        
        dicom_sr_path = os.path.splitext(os.path.basename(dicom_image_path))[0] + "_DICOM_SR.dcm"
        dicom_sr.save_as(os.path.join('results_dicom_rs', dicom_sr_path))
        
        
    # Send the DICOM SR to the local PACS OrthanC
    send_dicom_sr_to_pacs()
    