REST API Server
========



REST API Server for Cloud Provisioning Assistant

# Installation

## Pre-Requisites

Following pre-requisites are needed before installation:

- python3
- git
- docker
- mongodb

## Run Code

After the pre-requisites are installed, clone this repository using git and move into the repository by running: 

```bash
cd assistant-rest-apiserver
```

Then to build and run the code using docker:

```bash
sudo docker build  -t ashutoshdtu/assistant-rest-apiserver:0.1.0 .
sudo docker run --rm -p 8000:8000/tcp ashutoshdtu/assistant-rest-apiserver:0.1.0
```

Or using helm:

```bash
helm install --debug assistant-rest-apiserver ./charts/rest-apiserver
```
