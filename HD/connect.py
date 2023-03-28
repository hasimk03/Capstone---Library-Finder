import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import time as t
import math

class Azure_connection():
    def __init__(self):
        self.ghg =''
        self.storage_account_key = "hfhm6XhqHX4jV+OIUVNmD3O0JWsh3XYTCsnVjUlyTSUBx7t8hzIveHBY2mue0vPVt/6caDDjtQO1+AStu8z5+Q=="
        self.storage_account_name = "libraryfinderstorageacct"
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=libraryfinderstorageacct;AccountKey=hfhm6XhqHX4jV+OIUVNmD3O0JWsh3XYTCsnVjUlyTSUBx7t8hzIveHBY2mue0vPVt/6caDDjtQO1+AStu8z5+Q==;EndpointSuffix=core.windows.net"
        self.container_name = "test-room1"
        
        self.connect_to_storage_account()
    
    def connect_to_storage_account(self):
        try:
            account_url = "https://<libraryfinderstorageacct>.blob.core.windows.net"
            default_credential = DefaultAzureCredential()
            # Create the BlobServiceClient object
            blob_service_client = BlobServiceClient(account_url, credential=default_credential)
            print("Azure Blob Storage Python quickstart sample")
            # calling a function to perform upload
            self.uploadToBlobStorage('/Users/mahreenquadeer/desktop/mockData1.txt','mockData1.txt')
        except Exception as ex:
            print('Exception:')
            print(ex)


    def uploadToBlobStorage(self,file_path,file_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=file_name)
        
        with open(file_path,"rb") as data:
            print(f"Uploading {file_name} now.") 
            start = t.time()
            #blob_client.upload_blob(data,overwrite=True)
            exec = math.ceil(t.time()-start)
            print(f"Uploaded {file_name}. Upload took {exec} seconds")





def main():
    print("\nStart")
    conn = Azure_connection()
    conn.__init__()

if __name__ == "__main__":
    main()