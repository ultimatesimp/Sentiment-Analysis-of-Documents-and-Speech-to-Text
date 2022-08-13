

#Essentials
audio_filepath = "/Users/anveshsk/Dropbox/Final_summer_course/audio/" 
text_filepath = "/Users/anveshsk/Dropbox/Final_summer_course/Transcripts/"
bucket_name = "anvesh_demo"
project_id = "summercourse-356705"
endpoint_id = "8531005166797717504"
json_key = 'summercourse-356705-c2d5caafe2e5.json'

#Import libraries
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import storage
import wave
import os
import io
from sentiment_prediction import *


# Find the framerate and channels of audio file
def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels

#Set the channel to mono
def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)

#Dependency : pip install --upgrade google-cloud-storage. 
#Uploading audio file to bucket

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
     
    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(json_key
        )
    print("----------------------------------------------------------------------------------")
    print("\tUploading file to cloud... ")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file, timeout = (10,200))
    audio_file_name = blob.public_url.split("/")[-1]

    gcs_uri = 'gs://' + bucket_name + '/' + audio_file_name
    print("\tUPLOAD COMPLETE")
    print("-----------------------------------------------------------------------------------\n")
    
    #returns a gsutil uri
    return gcs_uri


#Delete file from bucket
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client.from_service_account_json(
        json_key)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    print("----------------------------------------------------------------------------------")
    print("\tDeleting file from bucket...")
    print("\tFILE DELETED")
    print("----------------------------------------------------------------------------------\n")
    blob.delete()


#Converting audio file to text
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
   

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    frame_rate, channels = frame_rate_channel(audio_full_path)
    if channels > 1:
        stereo_to_mono(audio_full_path)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        audio_channel_count=1,
        language_code ="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("----------------------------------------------------------------------------------")
    print("\tWaiting for operation to complete...")
    response = operation.result(timeout=90)

    print("\tTRANSCRIPT RECOVERED")
    print("----------------------------------------------------------------------------------\n")
    full_transcript = ''

    for result in response.results:
        full_transcript += result.alternatives[0].transcript

    return(full_transcript)
    


#Writing transcript onto a file
def write_transcripts(transcript_file_name,transcript):
    f= open(text_filepath + transcript_file_name,"w+")
    f.write(transcript)
    f.close()



if __name__ == "__main__":
    for audio_file_name in os.listdir(audio_filepath):
        if audio_file_name == ".DS_Store" :
            continue
        else : 
            print("----------------------------------------------------------------------------------")
            print("\tRetreiving file from local storage...")
            print("\tFILE RETRIEVED")
            print("----------------------------------------------------------------------------------\n")
            audio_full_path = audio_filepath + audio_file_name
            uri= upload_to_bucket(audio_file_name,audio_full_path, bucket_name)
            complete_transcript = transcribe_gcs(uri)
            transcript_file_name = audio_file_name.split('.')[0] + '.txt'

            write_transcripts(transcript_file_name,complete_transcript)


            delete_blob("anvesh_demo", audio_file_name)

            transcript_text = read_text_transcript(text_filepath, transcript_file_name)
            predict_text_sentiment_analysis_sample(project_id, endpoint_id, transcript_text)
            


  

