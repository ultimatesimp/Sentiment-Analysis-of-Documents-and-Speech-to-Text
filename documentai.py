#------------------------------------------------------------------------------------------------------------------------------------------
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
import os
#------------------------------------------------------------------------------------------------------------------------------------------


project_id= 'summercourse-356708'
location = 'us' # Format is 'us' or 'eu'
processor_id = 'key_here' #  Create processor in Cloud Console
file_path = input('Enter file path: ')
os.system('cls')
for i in file_path:
    if i == "'\'":
        i = '/'
endpoint_id = '6239798856372977664'

def quickstart(project_id: str, location: str, processor_id: str, file_path: str):

    temp = []
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    result = client.process_document(request=request)
    document = result.document

    document_pages = document.pages
    # Read the text recognition output from the processor
    print("The document contains the following paragraphs:")
    for page in document_pages:
        paragraphs = page.paragraphs
        for paragraph in paragraphs:
            print(paragraph)
            paragraph_text = get_text(paragraph.layout, document)
            temp.append(paragraph_text)
    return temp

def get_text(doc_element: dict, document: dict):

    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response
#-------------------------------------------------------------------------------------------------------------
def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
     
    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(
        'summercourse-356708-3dfb121f2395.json')
    print("Uploading file to cloud... ")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    audio_file_name = blob.public_url.split("/")[-1]

    gcs_uri = 'gs://' + bucket_name + '/' + audio_file_name
    
    #returns a gsutil uri
    return gcs_uri

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client.from_service_account_json(
        'summercourse-356708-3dfb121f2395.json')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    print("Deleting file from bucket...")

    blob.delete()

#------------------------------------------------------------------------------------------------------------------
def predict_text_sentiment_analysis_sample(
    project: str,
    endpoint_id: str,
    content: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
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
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/text_sentiment_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(dict(prediction))

response = quickstart(project_id, location, processor_id, file_path)
string = ''
for i in response:
    string+= i.strip() + ' '

os.system('cls')
print('--------------------------------------------------------------------------------')
print('Extracted Text: ')
print('--------------------------------------------------------------------------------')
print(string)
print('--------------------------------------------------------------------------------')
print('Prediction: ')
print('--------------------------------------------------------------------------------') 
predict_text_sentiment_analysis_sample(project_id, endpoint_id, string)
