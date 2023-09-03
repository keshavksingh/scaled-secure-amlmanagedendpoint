from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    OnlineRequestSettings,
    Model,
    Environment
)
from azure.identity import ClientSecretCredential

#Details of AzureML workspace
subscription_id = '<>'
resource_group = 'mlops'
workspace_name = 'amlws-cus'

tenant_id='<>'
client_id='<>'
client_secret="<>"

creds = ClientSecretCredential(tenant_id, client_id, client_secret)
ml_client = MLClient(credential=creds, subscription_id=subscription_id, resource_group_name=resource_group, workspace_name=workspace_name)

endpoint_name = "irisamlendpoint-cus"

endpoint = ManagedOnlineEndpoint(
    name = endpoint_name, 
    description="This is endpoint for IRIS Inferencing for Central US Region.",
    auth_mode="key"
)

model = Model(path="C:/scaled-secure-aml-endpoint/model.pkl")
env = Environment(conda_file="C:/scaled-secure-aml-endpoint/conda.yml",
                  image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest")

blue_deployment = ManagedOnlineDeployment(
    name="default",
    endpoint_name=endpoint_name,
    model=model,
    environment=env,
    scoring_script="score.py",
    code_path="C:/scaled-secure-aml-endpoint",
    instance_type="Standard_D2as_v4",
    instance_count=1
)

endpoint.traffic = {"default": 100}
endpoint_poller = ml_client.online_endpoints.begin_create_or_update(endpoint)
if endpoint_poller.result():
    print("Endpoint Creation Complete!")
    print(endpoint_poller.result())
    deployment_poller = ml_client.online_deployments.begin_create_or_update(deployment=blue_deployment)
    if deployment_poller.result():
        print("Deployment of Endpoint Complete!")
        print(deployment_poller.result())