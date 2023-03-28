import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def func1():
    try:
        print("Azure Blob Storage Python quickstart sample")

        # Quickstart code goes here

    except Exception as ex:
        print('Exception:')
        print(ex)


def main():
    print("\nStart")
    func1()

if __name__ == "__main__":
    main()