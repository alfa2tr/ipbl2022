#!/usr/bin/env python
"""Provides CRUD operations and basics functions to interact with Firebase Storage.

Given that the .json file with credentials was generated and is available, this 
script provides a function to make connection with the Firebase cloud storage 
(initialize), functions for CRUD operations, that is in this case, Upload 
(upload_file), Download (download_file), Move (move_file) and Delete (delete_file),
as well as other common purpose functions like check_local_path and list_files.
Note: Funtions were not tested for Windows systems.
"""
from firebase_admin import credentials, initialize_app, storage
from os.path import exists

from more_itertools import bucket

CREDENTIALS_PATH = "US223/alfa2tr-firebase-adminsdk-wy7cj-499495b929.json"

def initialize(credentials_path: str = CREDENTIALS_PATH) -> None:
    """Initializes access to firebase with your credentials.

    Args:
        credentials_path (str, optional): Path to a certificate file, most 
        likely a .json file, or a dict representing the contents 
        of a certificate. Defaults to CREDENTIALS_PATH.
    """
    cred = credentials.Certificate(credentials_path)
    initialize_app(cred, {'storageBucket': 'alfa2tr.appspot.com'})

def check_local_path(local_path: str) -> None:
    """Auxiliar function that asserts the existence of a given local file path.

    Args:
        local_path (str): Path in unix format to a file which existance needs 
        to be asserted.
    """
    try:
        assert exists(local_path)
    except:
        print("%s file doesn't exist" % local_path)

def upload_file(local_path : str, cloud_path : str="/"):
    """Given there's access to the firebase storage, makes the upload of local file
    to the firebase cloud storage.

    Args:
        local_path (str): Local path in unix format of the file.
        cloud_path (str, optional): Destination path in firebase cloud storage. If
        default path is passed, then it uploads to a path the same as local path. 
        Defaults to "/".
    """
    try:
        bucket = storage.bucket()
        if cloud_path == "/":
            if local_path.startswith("."):
                cloud_path = local_path.lstrip("./")
            else:
                cloud_path = local_path
        blob = bucket.blob(cloud_path)
        blob.upload_from_filename(local_path)

        print(f"File {local_path} has been uploaded as object {cloud_path}")
    except BaseException as err:
        print("Try running initialize()")
        print(err)

def download_file(cloud_path: str, local_path: str = "./") -> None:
    """Given there's access to the firebase storage, downloads a object from the 
    firebase storage.

    Args:
        cloud_path (str): Path of object (blob) in firebase storage.
        local_path (str, optional): Destination path, in unix format, to where 
        files will be downloaded. If folders to path don't exist, they be created. 
        If default path is passed, then files will follow the same structure as in 
        firebase storage. Defaults to "./".
    """
    bucket = storage.bucket()
    blob = bucket.blob(cloud_path)
    if local_path == "./":
        local_path += cloud_path.split("/")[-1]
    blob.download_to_filename(local_path)

    print(f"Downloaded object {cloud_path} to file {local_path}")

def copy_file(cloud_source_path: str, cloud_destination_path: str) -> None:
    bucket = storage.bucket()
    blob = bucket.blob(cloud_source_path)
    new_blob = bucket.copy_blob(blob, bucket, cloud_destination_path)

    print(f"Blob {blob.name} has been copy to {new_blob.name}")

def move_file(old_cloud_path: str, new_cloud_path: str) -> None:
    """Moves an object in firebase storage to a new path in the cloud. Functions the 
    same as UNIX's "mv" command, there is, it can also be used to rename an object.

    Args:
        old_cloud_path (str): Old path of object in firebase storage.
        new_cloud_path (str): New path of object in firebase storage.
    """
    bucket = storage.bucket()
    blob = bucket.blob(old_cloud_path)
    new_blob = bucket.rename_blob(blob, new_cloud_path)

    print(f"Blob {blob.name} has been renamed to {new_blob.name}")

def delete_file(cloud_path: str) -> None:
    """Deletes an object in firebase storage.

    Args:
        cloud_path (str): Path of object (blob) in firebase storage that you want
        to delete.
    """
    bucket = storage.bucket()
    blob = bucket.blob(cloud_path)
    blob.delete()

    print(f"Blob {blob.name} has been deleted.")

def list_files() -> list:
    """Lists all files in firebase storage.

    Returns:
        list: List of all files in firebase storage.
    """
    bucket = storage.bucket()
    blobs = bucket.list_blobs()

    return [blob.name for blob in blobs]

if __name__ == "__main__":
    initialize()
    upload_file("./Users/test.png")
    
    list_files()
