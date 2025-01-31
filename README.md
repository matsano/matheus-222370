# DICOM Processing and Classification using TorchXRayVision with Docker and PACS OrthanC

## Description

To complete this challenge, three Python scripts were implemented. The **publisher_DICOM.py** file sends DICOM files to an OrthanC server. Using these DICOM files, the **classification_DICOM.py** file computes classification results for findings using the pre-trained DenseNet model from the TorchXRayVision library. Finally, the **publisher_DICOM_SR.py** file creates a DICOM SR for each DICOM file with the model results and sends it to the local OrthanC PACS. The DICOM files are located in the *dicom_samples* folder.

Initially, the findings classification was implemented in the Jupyter Notebook **classification_DICOM.ipynb**, as it allows for better code organization and dataset visualization. To run your script with the Dockerfile, the code is available in the **classification_DICOM.py** file.

The *results_classification* folder contains the classification results in JSON files. The *results_dicom_sr* folder contains the DICOM SR files that were sent to the local OrthanC PACS.


## Execution

### 1) GitHub

Clone the repository:

```bash
git clone https://github.com/matsano/matheus-222370.git
cd matheus-222370
```

### 2) Dockerfile

To execute all the tasks required for the challenge, run the following commands in the terminal. Both the DICOM files and the DICOM_SR files will be available at http://localhost:8042 after execution. The login and password to access localhost are **orthanc**.

- Pull the image from Docker Hub
    ```bash
    docker pull jodogne/orthanc-python
    ```

- Create a new Docker network called *my-network*, allowing multiple containers to communicate
    ```bash
    docker network create my-network
    ```

- Create and start a Docker container based on the image from Docker Hub
    ```bash
    docker run -d --name orthanc --network my-network -p 4242:4242 -p 8042:8042 jodogne/orthanc-python
    ```

- Build a Docker image from the Dockerfile
    ```bash
    docker build -t python-scripts-test .
    ```

- Create and start a container, executing all implemented scripts and performing all required tasks: sending the DICOM files, classifying findings, and sending the DICOM_SR files.

    It may take around **30 seconds** for all scripts to execute and for the DICOM SR files to become visible at http://localhost:8042
    ```bash
    docker run -d --name python-scripts --network my-network python-scripts-test
    ```

- Copy the JSON files with classification results from the Docker container to the host system.
After executing this command, the JSON files will be available in the *results_classification* folder.
    ```bash
    docker cp python-scripts:/app/results_classification ./
    ```

- Execute the same command as above, but this time to copy the DICOM SR files to the *results_dicom_sr* directory.
    ```bash
    docker cp python-scripts:/app/results_dicom_sr ./
    ```

## Comments


Before taking on this challenge, I was not familiar with the Docker platform or the PACS archiving system.
To start, I focused on understanding how Docker works, learning how to download and run the OrthanC PACS ([link](https://github.com/jodogne/OrthancDocker)) using Docker, and how to execute a container. A helpful resource I found was this [link](https://medium.com/buildpiper/simplifying-containerization-with-docker-run-command-2f74e114f42a).

Next, I learned how to send DICOM files to the OrthanC PACS. During this step, encountered some difficulties interacting with localhost. However, after researching online, I identified the cause of the failure by analyzing the *status_code*. The issue was a simple mistake: I had not provided the authentication credentials required to access localhost. Once I corrected this, I was able to successfully send the DICOM files.

The third task was the most interesting to me, as I have a strong interest in medical applications in informatics.
This task gave me the opportunity to work with DICOM files and use a pre-trained model specifically designed for medical data.
Before performing classification with TorchXRayVision, I first visualized the dataset to better understand its structure and content. The resulting images can be seen in **classification_DICOM.ipynb**.
To classify findings in the DICOM files, I used a pre-trained model from TorchXRayVision. This library provides models such as DenseNet and ResNet. However, according to this paper [arxiv.org/abs/2002.02497](https://doi.org/10.48550/arXiv.2002.02497), DenseNet has proven to be the best architecture for predictive X-ray models. Therefore, I used DenseNet for this task.

The fourth and final task was the most challenging for me, as I was unfamiliar with DICOM SR files. To tackle this, I first researched what a DICOM SR file is and how to create one using a Python script. This task required more effort because I had to understand the meaning of each parameter in the DICOM SR format and how to set them correctly. To achieve this, I searched online and used ChatGPT to identify the relevant parameters for creating a DICOM SR file. When I attempted to send the files to the local PACS, I encountered a *status_code* 404 error. This could have been caused by an incorrect localhost URL or improperly formatted DICOM SR files. Upon reviewing my code, I found errors in the way some parameters were defined. After correcting them, I successfully sent the DICOM SR files to their respective patient/study/series in the PACS.

This activity gave me the opportunity to explore medical data types I had not worked with before, interact with storage systems used in medical environments, and learn about an AI model for X-ray imaging.
It further strengthened my interest in my research project, as I aim to specialize in biomedical research and tackle the challenges that arise in this field—just as I did during this experience.
