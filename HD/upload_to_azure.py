import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import time as t
import math

class Azure_connection():
    def __init__(self):
        self.ghg =''
        self.storage_account_key = ""                               #get from azure portal
        self.storage_account_name = "libraryfinderstorageacct"  
        self.connection_string = ""                                 #get from azure portal
        self.container_name = "test-room1"                          #dynamic for each location
        
        self.connect_to_storage_account()
    
    def connect_to_storage_account(self):
        try:
            account_url = "https://<libraryfinderstorageacct>.blob.core.windows.net"
            default_credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(account_url, credential=default_credential)     #create BlobServiceClient object
            print("Gathering Azure credentials")
            self.uploadToBlobStorage('full_file_direc','azure_data.txt')                            #enter directory
        except Exception as ex:
            print('Exception {ex} occured')


    def uploadToBlobStorage(self,file_path,file_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=file_name)
        
        with open(file_path,"rb") as data:
            print(f"Uploading {file_name} now.") 
            start = t.time()
            blob_client.upload_blob(data,overwrite=True)                                       #uploads data to container
            exec = math.ceil(t.time()-start)
            print(f"Uploaded {file_name}. Upload took {exec} seconds")

def main():
    conn = Azure_connection()
 
if __name__ == "__main__":
    main()