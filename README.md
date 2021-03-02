CLOUD PROVISIONING ASSISTANT
========

REST API Server for Cloud Provisioning Assistant

## DONE:

1. A REST API that is elegantly designed.
2. The system keeps track of each requests from the developers and waits for approval from DevOps team.
3. Once the system has provisioned the environment, the developer who requested the environment is notified. [MOCKED UP] Notifications are saved right now but not sent. 
4. Quota can be allocated, updated and enforced using a set of microservices.
5. Temporary and Permanent quota types available. 
6. Developers can request a one-time extension
7. All data is persisted during restarts.
8. Easy to debug and maintain.
9. Externalized config, health check.

## TODOS:

1. Implement the following Redis queue consumer services:

    * **Analyse Provision Request**
    * **Provision Resource:** Do actual provisioning & produce kubeconfig
    * **Purge Resource**

2. Add Jobs to queue
3. Send actual notifications.
4. Integrate with AWS IAM or Implement ACL.
5. Add support for services other than kubernetes.
6. Send notifications to developers when their environment is about to expire.
7. Web based UI.

## DESIGN DECISIONS:

**1. Microservices pattern:** RESTful (and Event sourcing

**2. DB:** MongoDB

**Reason:** Flexible schema, quicker proof of concept. 

Installed using helm charts.

**3. Queue:** Redis (with persistence)

**Requirements:** persistence, resilience, highly available

Helm chart from bitnami was used which has persistence, sentinel and various cluster paradigms available. 

**4. REST API features:**

* HATEOAS compliant APIs
* OpenAPI 3 specifications available on ```/api-docs```
* REST API docs available on ```/docs```
* Externalized configuration ```settings.ini```
* Helm chart available
* provides rich filter, sort, embed, PATCH and many other features using Python Eve. 

**5. Microservices features:**

* Kubernetes ready
* One command to deploy (helm install <>)
* Can autoscale
* All data is persisted during restarts


## STEPS TO DEPLOY

### 1. Get dependencies

**Install helm:**

```
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```
or
```
$ brew install helm
```
Official installation docs: https://helm.sh/docs/intro/install/

**Install httpie (optional):**

Install httpie using your favourite package manager:

```
$ brew install httpie
$ apt-get install httpie
$ pip install httpie
$ yum install httpie
```

### 2. Install and run mongodb

```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install mongodb -f ./charts/mongodb/values.yaml bitnami/mongodb
```
To uninstall 
```
$ helm uninstall mongodb
```

### 3. Install and run rest-apiserver

```
$ helm install --debug assistant-rest-apiserver ./charts/rest-apiserver
$ kubectl port-forward service/assistant-rest-apiserver 8000:8000
```
To uninstall
```
$ helm uninstall assistant-rest-apiserver
```

**To build and run the code using docker:**

```bash
$ sudo docker build  -t ashutoshdtu/assistant-rest-apiserver:0.1.0 .
$ sudo docker run --rm -p 8000:8000/tcp ashutoshdtu/assistant-rest-apiserver:0.1.0
```

### 4. Install redis
```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install redis \
  --set master.persistence.size=200Mi \
  --set usePassword=false \
  # --set cluster.enabled=true  --set cluster.slaveCount=3 \
    bitnami/redis
```

### 5. Pre-populate db
```
$ http POST 127.0.0.1:8000/v1/roles role=admin description=Admin
$ http POST 127.0.0.1:8000/v1/roles role=dev description=Developer
$ http POST 127.0.0.1:8000/v1/roles role=devops description=DevOps

$ http POST 127.0.0.1:8000/v1/users name=AAA email=aaa@xyz.com username=aaa roles:='["admin"]'
$ http POST 127.0.0.1:8000/v1/users name=BBB email=bbb@xyz.com username=bbb roles:='["dev"]'
$ http POST 127.0.0.1:8000/v1/users name=CCC email=ccc@xyz.com username=ccc roles:='["dev"]'
$ http POST 127.0.0.1:8000/v1/users name=DDD email=ddd@xyz.com username=ddd roles:='["dev"]'
$ http POST 127.0.0.1:8000/v1/users name=EEE email=eee@xyz.com username=eee roles:='["dev"]'
$ http POST 127.0.0.1:8000/v1/users name=JJJ email=jjj@xyz.com username=jjj roles:='["devops"]'
$ http POST 127.0.0.1:8000/v1/users name=KKK email=kkk@xyz.com username=kkk roles:='["devops"]'
$ http POST 127.0.0.1:8000/v1/users name=LLL email=lll@xyz.com username=lll roles:='["devops"]'

$ http POST 127.0.0.1:8000/v1/templates \
    _id="basic-eks-cluster" name="Basic EKS Cluster" \
    clusteryaml="https://raw.githubusercontent.com/ashutoshdtu/assistant-rest-apiserver/main/app/src/rest_apiserver/models/eksctl_templates/basic-eks-cluster.yaml" \
    params:='["cluster_name", "region", "instance_type", "desired_capacity", "volume_size"]'
```

The following requests will not work directly (ids are randomly assigned) but can be used as samples:
```
## Provision Request
$ http POST 127.0.0.1:8000/v1/provisionRequests \
    description="2 node k8s cluster of t2.micro instances" \
    expires_by="Wed, 03 Mar 2021 23:32:43 GMT" \
    requested_by="603d32d7f8d6f8da9927f0b2" \
    resource_type="KUBERNETES" \
    resource_template="basic-eks-cluster" \
    resource_parameters:='{"cluster_name":"dev-cluster-2", "region":"us-west-1", "instance_type": "t2.micro", "desired_capacity": 2, "volume_size": 30 }'

## Provision reviews
$ http POST 127.0.0.1:8000/v1/approveProvisionRequest _id="603d6899ec8c768ca04fa9f4" reviewed_by="603d334bf8d6f8da9927f0b4" status="REJECTED"

$ http POST 127.0.0.1:8000/v1/approveProvisionRequest _id="603d6990ec8c768ca04fa9f5" reviewed_by="603d334bf8d6f8da9927f0b4" status="APPROVED"

## Extension Requests
$ http POST 127.0.0.1:8000/v1/extensionRequests \
    reason="Delay in project." \
    extend_by="48" \
    requested_by="603d32d7f8d6f8da9927f0b2" \
    provision_request="603d6990ec8c768ca04fa9f5"

## Extension reviews
$ http POST 127.0.0.1:8000/v1/approveExtensionRequest _id="603d7484f0b3b48214b53f18" reviewed_by="603d334bf8d6f8da9927f0b4" status="APPROVED"
```

## API Documentation

Full API documentation can be found on ```/docs``` route but you can also check out PDF:
https://github.com/ashutoshdtu/assistant-rest-apiserver/raw/main/API%20documentation.pdf

```v1/approveProvisionRequest``` and ```v1/approveExtensionRequest``` are yet to be added to the documentation. 

### ```v1/approveProvisionRequest```:

**HTTP method:** POST
**Request:**

```json
{
    "_id": "<id>",              # Provision request id
    "reviewed_by": "<userid>",  # Reviewer user id
    "status": "APPROVED"        # APPROVED or REJECTED
}
```

**Response:**
```json
{
    "status": "APPROVED",
    "_id": "<id>"
}
```

### ```v1/approveExtensionRequest```:

**HTTP method:** POST
**Request:**

```json
{
    "_id": "<id>",              # Provision request id
    "reviewed_by": "<userid>",  # Reviewer user id
    "status": "REJECTED"        # APPROVED or REJECTED
}
```

**Response:**
```json
{
    "status": "REJECTED",
    "_id": "<id>"
}
```