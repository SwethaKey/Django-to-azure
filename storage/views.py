from django.shortcuts import render, redirect
from .form import FileUploadForm
from azure.storage.blob import BlobServiceClient
import os
from django.conf import settings
 
# Create your views here.
# Azure Blob Storage settings
connection_string = "DefaultEndpointsProtocol=https;AccountName=swethastore234;AccountKey=8UA2tJWx0/Xy9ztqvEGlfWVVt8FxZVSLZxinbu6E9NPtDZP4Ncx+XRJppah6Z2A4pDddH2bprxYp+AStZ8vzdQ==;EndpointSuffix=core.windows.net"
container_name = "pictures"
 
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
 
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.name)
            blob_client.upload_blob(file.read())
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
 
def file_list(request):
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    return render(request, 'list.html', {'blobs': blob_list})
 
def download_file(request, blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    # Define the path to save the file in the static folder
    download_file_path = os.path.join(settings.BASE_DIR, 'static', blob_name)
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
   # download_file_path = f"{blob_name}"
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    return redirect('file_list')
 
