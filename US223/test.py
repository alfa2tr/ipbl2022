#!/usr/bin/env python
"""Provides CRUD operations and basics functions to interact with Firebase Storage.

Given that the .json file with credentials was generated and is available, this 
script provides a function to make connection with the Firebase cloud storage 
(initialize), functions for CRUD operations, that is in this case, Upload 
(upload_file), Download (download_file), Move (move_file) and Delete (delete_file),
as well as other common purpose functions like check_local_path and list_files.
"""
from firebase_admin import credentials, initialize_app, storage
from os.path import exists

CREDENTIALS_PATH = "friendly-chat-test-alfa2tr-firebase-adminsdk-tu82o-7dec33160d.json"

def initialize(credentials_path: str = CREDENTIALS_PATH) -> None:
    """Initialize access to firebase with your credentials.
    
    credentials_path: Path to a certificate file, most 
    likely a .json file, or a dict representing the contents 
    of a certificate.
    """
    cred = credentials.Certificate(credentials_path)
    initialize_app(cred, {'storageBucket': 'friendly-chat-test-alfa2tr.appspot.com'})

def check_local_path(local_path: str) -> None:
    """Asserts the existence of a given local file path.
    
    local_path: Path to a file which existance needs to be
    asserted.

    Note: local_path should be in unix format. 
    """
    try:
        assert exists(local_path)
    except:
        print("%s file doesn't exist" % local_path)

def upload_file(local_path : str, cloud_path : str="/"):
    try:
        bucket = storage.bucket()
        if cloud_path == "/":
            if local_path.startswith("."):
                cloud_path = local_path.lstrip("./")
            else:
                cloud_path += local_path
        blob = bucket.blob(cloud_path)
        blob.upload_from_filename(local_path)

        print(f"File {local_path} has been uploaded as object {cloud_path}")
    except:
        print("Try running initialize()")

def download_file(cloud_path, local_path="./"):
    bucket = storage.bucket()
    blob = bucket.blob(cloud_path)
    if local_path == "./":
        local_path += cloud_path.split("/")[-1]
    blob.download_to_filename(local_path)

    print(f"Downloaded object {cloud_path} to file {local_path}")

def move_file(old_cloud_path, new_cloud_path):
    bucket = storage.bucket()
    blob = bucket.blob(old_cloud_path)
    new_blob = bucket.rename_blob(blob, new_cloud_path)

    print(f"Blob {blob.name} has been renamed to {new_blob.name}")

def delete_file(cloud_path):
    bucket = storage.bucket()
    blob = bucket.blob(cloud_path)
    blob.delete()

    print(f"Blob {blob.name} has been deleted.")

def list_files():
    bucket = storage.bucket()
    blobs = bucket.list_blobs()

    return [blob.name for blob in blobs]

if __name__ == "__main__":
    initialize()
    upload_file("./Users/test.png")
    
    list_files()
