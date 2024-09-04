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
    
    # Configurar os metadados do arquivo DICOM, identificando o tipo de dados presentes no arquivo DICOM
    dicom_sr.file_meta = FileMetaDataset()
    dicom_sr.file_meta.MediaStorageSOPClassUID = EnhancedSRStorage
    dicom_sr.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    dicom_sr.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    
    # Um SOP Class é uma classe que define o tipo de dados e as operacoes que podem ser realizadas sobre esses dados.
    # Logo, deve-se definir a SOP Class como Enhanced Structured Report
    dicom_sr.SOPClassUID = EnhancedSRStorage
    dicom_sr.SOPInstanceUID = generate_uid()
    
    # Definir o conteúdo do arquivo DICOM sendo um Structured Report
    dicom_sr.Modality = "SR"
    
    # Adicionar informacoes que identificam paciente, estudo e serie
    dicom_sr.PatientName = dicom_image.PatientName
    dicom_sr.PatientID = dicom_image.PatientID
    dicom_sr.StudyInstanceUID = dicom_image.StudyInstanceUID
    dicom_sr.SeriesInstanceUID = dicom_image.SeriesInstanceUID
    
    # Add structured report content
    dicom_sr.ContentSequence = []
    for task, probability in json_results.items():
        # Adicionar um novo objeto Dataset para armazenar os dados relacionados a uma doenca especifica
        item = Dataset()
        
        # Definir a sequencia de codigo conceito para uma task
        item.ConceptNameCodeSequence = [Dataset()]
        item.ConceptNameCodeSequence[0].CodeValue = 'Task'
        item.ConceptNameCodeSequence[0].CodeMeaning = task
        
        # Definir o sistema de codificacao como DCM, usado para codigos definidos especificamente no padrao DICOM,
        # sem a necessidade de serem representados por um sistema de codificacao clinico padrao
        item.ConceptNameCodeSequence[0].CodingSchemeDesignator = 'DCM'
        
        # Definir a unidade de medida para o valor medido
        item.MeasurementUnitsCodeSequence = [Dataset()]
        item.MeasurementUnitsCodeSequence[0].CodeValue = 'PERCENT'
        item.MeasurementUnitsCodeSequence[0].CodeMeaning = 'Percent'
        
        # O sistema de codificacao eh o UCUM, usado para representar unidades de medida
        item.MeasurementUnitsCodeSequence[0].CodingSchemeDesignator = 'UCUM'
        
        # Armanzear a probabilidade correspondente a task
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
    