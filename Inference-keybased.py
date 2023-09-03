import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
data =  {
  "input_data": "[[5.1,3.5,1.4,0.2],[7,3.2,4.7,1.4],[6.3,3.3,6,2.5]]"
}
#Setosa,Versicolor,Virginica
body = str.encode(json.dumps(data))
url = 'https://irisamlendpoint.eastus.inference.ml.azure.com/score'
api_key = 'aBFF7y3PNyzOfNdMVofcAOeIZz4XRQqk'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'iris-random-forest-model-1' }
req = urllib.request.Request(url, body, headers)
try:
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))