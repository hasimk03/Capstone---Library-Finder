import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

#Cannot run this file without host microsoft login [Run app on host computer for initial deployment]

#Add 'import download_from_azure as azure' to import this file 
#Call azure.main() to grab real time data 
#data will then be stored in directory given in self.local_path in the file 'DOWNLOAD.txt'

class Azure_connection():
    def __init__(self): 
        self.local_path = r"C:\Users\Hasimk\Documents\GitHub\Capstone---Library-Finder"         #UPDATE TO YOUR WORKING DIRECTORY
        self.storage_account_name = "libraryfinderstorageacct"  
        self.connection_string = ""                                 #get from azure portal
        self.container_name = "test-room1"                          #dynamic for each location
        self.blob_name = 'azure_data.txt'                           #file name inside container
        self.connect_to_storage_account()
            
    def connect_to_storage_account(self):
        try:
            account_url = "https://<libraryfinderstorageacct>.blob.core.windows.net"                #Azure storage account url
            default_credential = DefaultAzureCredential()
            blob_service_client = BlobServiceClient(account_url, credential=default_credential)     #create BlobServiceClient object
            print("Gathering Azure credentials")
            self.download_file()
        except Exception as ex:
            print('Exception {} occured'.format(ex))


    def download_file(self):
        download_file_path = os.path.join(self.local_path,r'DOWNLOAD.txt')                          #create full path for downloaded file
        
        #Connect to Azure and specific test room container via attributes
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)      
        container_client = blob_service_client.get_container_client(container=self.container_name) 
        
        print("\nDownloading blob to \n\t" + download_file_path)
        with open(file=download_file_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob(self.blob_name).readall())          #read azure file and write to local file

def main():
    conn = Azure_connection()
 
if __name__ == "__main__":
    main()

