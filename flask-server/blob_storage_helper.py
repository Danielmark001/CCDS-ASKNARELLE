from azure.storage.blob import BlobServiceClient,generate_blob_sas, BlobSasPermissions
import os
from urllib.parse import quote
from datetime import datetime, timedelta


connection_string = os.environ.get('AZURE_CONN_STRING')
storage_account_name = "sc1015filestorage"
storage_account_key = os.environ.get('AZURE_STORAGE_KEY')

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def createContainer(containerName):
    try:
        container_client = blob_service_client.create_container(containerName.lower())
        print(f"Container created successfully. Request ID: {container_client.container_name}")
        return True
    except Exception as error:
        print(f"Error creating container: {error}")
        return False

def delete_blob_storage_container(containerName):
    try:
        container_client = blob_service_client.get_container_client(containerName.lower())
        container_client.delete_container()
        print("Container deleted successfully.")
        return True
    except Exception as error:
        print(f"Error deleting container: {error}")
        return False
    
def upload_to_azure_blob_storage(containerName, files):
    try:
        container_client = blob_service_client.get_container_client(containerName)

        # List and delete existing blobs with the "new/" prefix
        blobs_list = container_client.list_blobs(name_starts_with="new/")
        for blob in blobs_list:
            blob_client = container_client.get_blob_client(blob)
            blob_client.delete_blob()
            print(f"Deleted blob: {blob.name}")
        
        for file in files:
            # Upload to "new/" folder
            blob_client_in_folder = container_client.get_blob_client(f"new/{file.filename}")
            file.seek(0)  # Ensure the file stream is at the beginning
            upload_response1 = blob_client_in_folder.upload_blob(file, overwrite=True)
            print(f"File uploaded successfully to folder. Request ID: {upload_response1['request_id']}")
            
            # Upload directly to the container root
            blob_client_direct = container_client.get_blob_client(f"{file.filename}")
            file.seek(0)  # Reset the file stream again to the beginning
            upload_response2 = blob_client_direct.upload_blob(file, overwrite=True)
            print(f"File uploaded successfully to container. Request ID: {upload_response2['request_id']}")
        
        return True
    except Exception as error:
        print(f"Error uploading file: {error}")
        return False
    

def delete_from_azure_blob_storage(containerName, blobName):
    try:
        # Get a reference to the container
        container_client = blob_service_client.get_container_client(containerName)

        # Get a block blob client
        blob_client = container_client.get_blob_client(blobName)
        blobName = 'new/'+blobName
        container_client
        blob_client_new = container_client.get_blob_client(blobName)
        print('hey')
        if blob_client_new.exists():
            blob_client_new.delete_blob()
        # Delete the blob
        blob_client.delete_blob()
        print(f"File deleted successfully")
        return True
    except Exception as error:
        print(f"Error deleting file: {error}")
        return False

def generate_sas_token(container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # Adjust expiry time as needed
    )
    return sas_token