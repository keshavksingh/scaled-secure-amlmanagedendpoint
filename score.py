import os
import logging
import json
import pickle
import ast

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # Please provide your model's folder name if there is one
    global loaded_model
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "model.pkl"
    )
    loaded_model = pickle.load(open(model_path, 'rb'))
    logging.info("Init complete")

def run(input: str):
    input = ast.literal_eval(input)
    print(input)
    target_names=['setosa' ,'versicolor' ,'virginica']
    predVal = input #[[5.9,3.,5.1,1.8]] #Sepal Lenght, Sepal Width, Petal Lenght, Petal Width
    prediction = loaded_model.predict(predVal)
    prediction = [round(p) for p in prediction]
    prediction = [target_names[p] for p in prediction]
    result_json = json.dumps({"result":str(prediction)})
    print("Output Response String - !")
    print(result_json)
    logging.info("Request processed")
    return result_json
