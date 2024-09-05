# matheus-222370

## Descrição

Para a realização desse desafio foram implementados 3 scripts python. O arquivo **publisher_DICOM.py** envia arquivos DICOM para um servidor OrthanC. A partir desses arquivos DICOM, o arquivo **classification_DICOM.py** compulta os resultados de classificação de achados utilizando o modelo pré-treinado DenseNet da biblioteca TorchXRayVision. Por fim, o arquivo **publisher_DICOM_SR** cria um DICOM SR para cada arquivo DICOM com os resultados dos modelos e o envia para o PACS local OrthanC. Os arquivos DICOM se encontram na pasta *dicom_samples*.

Inicialmente, a classificação de achados foi implementada no Jupyter Notebook **classification_DICOM.ipynb**, pois é possível organizar o código e visualizar melhor o dataset. Para executar seu script com o Dockerfile seu código se encontra no arquivo **classification_DICOM.py**.

A pasta *results_classification* contém os resultados da classificação de achados em arquivos JSON. A pasta *results_dicom_sr*, por sua vez, contém os arquivos DICOM SR que foram enviados para o PACS local OrthanC.


## Execução

### 1) GitHub

Clonar o repositório:

```bash
git clone https://github.com/matsano/matheus-222370.git
cd matheus-222370
```

### 2) Dockerfile

Para executar todas as tarefas exigidas pelo desafio deve-se rodar os seguintes comandos no terminal. Tanto os arquivos DICOM quanto os arquivos DICOM_SR poderão ser encontrados em http://localhost:8042 depois da execução dos comandos. Tanto o login e quanto a senha para acessar o localhost é **orthanc**.

- Obter imagem do Docker Hub
    ```bash
    docker pull jodogne/orthanc-python
    ```

- Criar uma nova rede Docker chamada *my-network*, permitindo que múltiplos contêineres se comuniquem entre si
    ```bash
    docker network create my-network
    ```

- Criar e iniciar um contêiner Docker com base na imagem obtida do Docker Hub
    ```bash
    docker run -d --name orthanc --network my-network -p 4242:4242 -p 8042:8042 jodogne/orthanc-python
    ```

- Criar uma imagem Docker a partir do Dockerfile
    ```bash
    docker build -t python-scripts-test .
    ```

- Criar e iniciar um contêiner, executando todos os códigos implementados e realizando todas as tarefas solicitadas: envio dos arquivos DICOM, a classificação de achados e o envio dos arquivos DICOM_SR.

    Pode demorar em torno de **30 segundos** para executar todos os códigos e os arquivos DICOM SR serem visíveis no http://localhost:8042
    ```bash
    docker run -d --name python-scripts --network my-network python-scripts-test
    ```

- Copiar do contêiner Docker para o sistema host os arquivos JSON com os resultados da classificação. Ao executar esse comando, os arquivos JSON poderão ser encontrados na pasta *results_classification*
    ```bash
    docker cp python-scripts:/app/results_classification ./
    ```

- Realizar o mesmo comando que o anterior, porém, nesse caso, são copiados os arquivos DICOM SR para o diretório *results_dicom_sr*
    ```bash
    docker cp python-scripts:/app/results_dicom_sr ./
    ```

## Comentários

Antes de realizar o desafio, eu não era familiarizado com a plataforma Docker e com o sistema de arquivamento PACS. Dessa forma, inicialmente, eu procurei entender melhor como funciona o Docker, além de aprender como baixar e rodar o PACS OrthanC ([link](https://github.com/jodogne/OrthancDocker)) por meio do Docker e como executar um container. Um site que me ajudou foi [link](https://medium.com/buildpiper/simplifying-containerization-with-docker-run-command-2f74e114f42a).

Em seguida, procurei aprender como enviar arquivos DICOM para o PACS OrthanC. Nessa etapa, eu tive um pouco de dificuldade em interagir com o localhost, porém pesquisando na internet eu pude identificar por meio do *status_code* o motivo da falha no envio. O motivo, em questão, foi um erro simples por não ter inserido as credenciais de autenticidade para acessar o localhost. Assim, pude corrigir esse erro e enviar os arquivos DICOM com sucesso.

O terceiro exercício foi o que eu achei mais interessante, pois eu tenho um grande interesse em aplicações médicas na informática e, nesse exercício, tive a oportunidade de aprender a interagir com arquivos DICOM e usar um modelo pré-treinado especificamente com dados médicos. Antes de realizar a classificação com TorchXRayVision, achei pertinente uma visualização inicial do conjunto de dados para ajudar a entender a estrutura e o conteúdo dos dados. As imagens obtidas podem ser vistas no **classification_DICOM.ipyn**. Para calcular a classificação dos achados dos arquivos DICOM, foi usado um modelo pré-treinado da TorchXRayVision. Esta biblioteca tem modelos pré-treinados como DenseNet e ResNet. No entanto, de acordo com o artigo [arxiv.org/abs/2002.02497](https://doi.org/10.48550/arXiv.2002.02497), DenseNets provou ser a melhor arquitetura para modelos preditivos de raios X. Portanto, DenseNet é usado para executar a tarefa.

O quarto e o último exercício foi o mais desafiador para mim, pois não conhecia sobre arquivos DICOM SR. Portanto, eu procurei entender o que é um arquivo DICOM SR e como criá-lo por meio de um script python. Esse exercício foi mais trabalhoso, pois eu tive que entender o que representava cada um dos parâmetros do DICOM SR e como setá-los de forma correta. Para isso, eu precisei pesquisar na internet e usar o ChatGPT para entender quais eram os parâmetros relevantes na criação de um arquivo DICOM SR. Ao tentar enviá-los para o PACS local, eu obtive o *status_code* 404. Esse erro poderia ser proveniente de uma falha em reconhecer a URL do localhost ou os arquivos DICOM SR não foram formatados corretamente. De fato, ao revisar o código, eu tinha alguns erros ao definir alguns parâmetros. Ao corrigi-los, o envio dos arquivos DICOM SR foi feito com sucesso no seu respectivo paciente/estudo/série.

Essa atividade me proporcionou a oportunidade de explorar tipos de dados médicos com os quais eu ainda não havia trabalhado, de interagir com sistemas de armazenamento usados em ambientes médicos e de conhecer um modelo de IA voltado para imagens de raio X. Isso aumentou meu interesse pelo tema da iniciação científica, pois busco me aprofundar justamente no campo da pesquisa biomédica e, assim, enfrentar os desafios que surgirão ao longo dessa experiência, como os que já encontrei nesta atividade.

Obrigado pela oportunidade de participar nessa segunda parte do processo.
