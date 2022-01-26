# kubernetes-fastapi

Template for a Python FastAPI with Dockerfile and configuration for Kubernetes

## structure 
 1. App : python api to replace word

 2. Resources : 
        a. architecture.drawio.png : Solution architecture
        
        b. azuredeploy.json : ARM template to deploy AKS cluster
        
        c. deploy.parameters.json : Parameter file for AKS arm
        
        d. pipeline-deploy.yaml : Yaml file for deployment Pipeline in azure devops
        
        e. pipeline-dockerbuild.yaml : Yaml pipeline for Building docker image and pushing image in ACR
        
        f. word-replace.PNG : Sample output after tunning docker file
    
3. api.yaml : Yaml file to create kubernetes deployment and service

4. autoscale.yaml : yaml pipeline to autoscale pods 

5. dockerfile : Dockerfile to create app container

6. requirements.txt : Dependencies required to run python code.


## Development setup

To run (in isolation), either:

Run from active Python environment using `uvicorn`:

    pip install -r requirements.txt
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

Or build and run the Docker container:

    docker build -t word-replace-api:latest .
    docker run -p 8080:8080 --name word-replace-api word-replace-api:latest

Navigate to http://localhost:8080/docs to test the API.


![Test drive the API](./resources/word-replace.PNG)

The API responds with a Get parameter test_str, and the result of the input "We really like the new security features of Google Oracle Microsoft Deloitte Amazon  Cloud"
You should see a response body similar to:

"We really like the new security features of Google© Oracle© Microsoft© Deloitte© Amazon©  Cloud"

## Push the container image to Docker Hub or azure container registry

    docker push word-replace:latest

    docker push myregistry.azurecr.io/word-replace:latest


## Azure Cloud AKS initial setup

Follow the steps in this section if deploying to Azure Cloud AKS. From command line, with [Azure CLI](https://docs.microsoft.com/nl-nl/cli/azure/install-azure-cli) installed:

Login to Azure Account
    az login
Create Resource Group
    az group create --name word-replace-rg --location eastus

Create a cluster and get credentials for `kubectl`:

    az aks create --resource-group word-replace-rg --name word-replace --node-count 1 --generate-ssh-keys
    az aks get-credentials --resource-group TestResourceGroup --name TestAKSCluster

Install Kubectl Utility
    az aks install-cli

## Connect ACR to AKS

   AKS_NAME=youraksname
   
   ACR_NAME=youracrname
   
   RG_NAME=your_resource_group_name

   az aks update -n $AKS_NAME -g $RG_NAME \
      --attach-acr $(az acr show -n $ACR_NAME --query "id" -o tsv)
      
## Kubernetes deployment

    kubectl apply -f api.yaml

If working locally, e.g. using `minikube`, use port forwarding to expose the service:

    kubectl port-forward service/word-replace-api-svc 8080

To scale the deployment, apply a HorizontalPodAutoscaler. Either:

    kubectl apply -f autoscale.yaml

or:

    kubectl autoscale deployment word-replace-api --cpu-percent=50 --min=1 --max=10


## Teardown

    kubectl delete deployment word-replace-api
    kubectl delete svc word-replace-api-svc
    kubectl delete hpa word-replace-api-hpa



