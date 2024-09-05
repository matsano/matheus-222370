# matheus-222370

## Descrição

Para a realização desse desafio foram implementados 3 scripts python. O arquivo **publisher_DICOM.py** envia arquivos DICOM para um servidor OrthanC. A partir desses arquivos DICOM, o arquivo **classification_DICOM.py** compulta os resultados de classificação de achados utilizando o modelo pré-treinado DenseNet da biblioteca TorchXRayVision. Por fim, o arquivo **publisher_DICOM_SR** cria um DICOM SR para cada arquivo DICOM com os resultados dos modelos e o envia para o PACS local OrthanC. Os arquivos DICOM se encontram na pasta *dicom_samples*.

Inicialmente, a classificação de achados foi implementada no Jupyter Notebook **classification_DICOM.ipynb**, pois é possível organizar o código e visualizar melhor o dataset. Para executar seu script com o Dockerfile seu código se encontra no arquivo **classification_DICOM.py**.

A pasta *results_classification* contém os resultados da classificação de achados em arquivos JSON. A pasta *results_dicom_sr*, por sua vez, contém os arquivos DICOM SR que foram enviados para o PACS local OrthanC.


## Execução

### 1) GitHub

Clonar o repositório com o seguinte comando:

```bash
git clone https://github.com/matsano/matheus-222370.git
```

### 2) Dockerfile

Para executar todas as tarefas exigidas pelo desafio deve-se rodar os seguintes comandos no terminal:

```bash
docker pull jodogne/orthanc-python
```

```bash
docker network create my-network
```

```bash
docker run -d --name orthanc --network my-network -p 4242:4242 -p 8042:8042 jodogne/orthanc-python
```

```bash
docker build -t python-scripts-test .
```

```bash
docker run -d --name python-scripts --network my-network python-scripts-test
```

```bash
docker cp python-scripts:/app/results_classification ./
```

```bash
docker cp python-scripts:/app/results_dicom_sr ./
```

## Comentários

1)

Antes de realizar o desafio, eu ainda não tinha trabalhado com a plataforma Docker e o sistema de arquivamento PACS. Dessa forma, inicialmente, eu procurei entender como funciona o Docker, além de aprender como baixar e rodar o PACS OrthanC ([link](https://github.com/jodogne/OrthancDocker)) por meio do Docker e como executar um container. Um site que me ajudou foi [link](https://medium.com/buildpiper/simplifying-containerization-with-docker-run-command-2f74e114f42a).

Em seguida, procurei aprender como enviar arquivos DICOM para o PACS OrthanC. Nessa etapa, eu tive um pouco de dificuldade em interagir com o localhost, porém pesquisando na internet eu pude identificar por meio do *status_code* o motivo da falha no envio. O motivo, em questão, foi um erro simples por não ter inserido as credenciais de autenticidade para acessar o localhost. Assim, pude corrigir esse erro e enviar os arquivos DICOM com sucesso.



