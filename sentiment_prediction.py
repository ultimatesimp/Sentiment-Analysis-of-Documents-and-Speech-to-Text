from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import os



#Dependency : pip install --upgrade google-cloud-aiplatform
#Predict the sentiment of a block of text through Vertex AI's endpoint 
def predict_text_sentiment_analysis_sample(
    project: str,
    endpoint_id: str,
    content: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    print("----------------------------------------------------------------------------------")
    print("\tPredicting the response...")
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = predict.instance.TextSentimentPredictionInstance(
        content=content,
    ).to_value()
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

 
    #print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/text_sentiment_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions

    for prediction in predictions:
        print("\tPREDICTION :", dict(prediction))
        print("----------------------------------------------------------------------------------\n")
        print("******************************************************************************************\n")
    
    
#Read the text from the file
def read_text_transcript(text_filepath, transcript_file_name):
    for text_file_name in os.listdir(text_filepath):
        if text_file_name == ".DS_Store" :
            continue
        else : 
            if text_file_name == transcript_file_name :
                print("----------------------------------------------------------------------------------")
                print("\tReading the transcript...\n")
                text_file_name = text_filepath + text_file_name
                f= open(text_file_name,"r")
                transcript_text = f.read()
                print(transcript_text)
                f.close()
                print("\n\tTRANSCRIPT READ")
                print("----------------------------------------------------------------------------------\n")
    
    return(transcript_text)