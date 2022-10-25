import os
import firebase_operations as fop
from playsound import playsound
from list_user_files import list_of_local_files, get_file_name_from_path

def us223_ct1():
    print("========== US223 - CT1 ==========")
    try:
        list_ = None
        list_ = fop.list_files()
        if list_ != None:
            print("Local dispositive is connected to remote storage.")
    except BaseException as err:
        print("Local dispositive is not connected to remote storage: ", err)
    finally:
        print()

def us223_ct2():
    print("========== US223 - CT2 ==========")
    try:
        list_of_local_paths = list_of_local_files("US223/Users")
    except:
        print("Local files were not found.")

    print("*Uploading files")
    for file_path in list_of_local_paths:
        fop.upload_file(file_path)
    print()
    
    print("*List of files in firebase storage")
    list(map(print, fop.list_files()))
    print()

    while True:
        delete = input("*Delete uploaded files? (Y/n): ")
        if delete == "Y" or delete == "y":
            for file_path in list_of_local_paths:
                fop.delete_file(file_path)
            break
        elif delete == "N" or delete == "n":
            break
        else:
            print("Unknown option.")
    print()

def us223_ct3():
    print("========== US223 - CT3 ==========")
    try:
        cloud_path_list = list_of_local_files("US223/Users")
        destination_path_list = []
        print("*Making copies of files for testing.")
        for path in cloud_path_list:
            destination_path = path.split("/")
            destination_path = "/".join(destination_path[:-2] + ["Test"] + destination_path[-1:])
            destination_path_list.append(destination_path)
            fop.copy_file(path, destination_path)
    except BaseException as err:
        print("Cloud object doesn't exist.")
        print(err)

    print("\n*List of files in firebase storage.")
    list(map(print, fop.list_files()))
    print()

    # Download copied files
    print("*Downloading files.")
    local_path_list = list(map(get_file_name_from_path, destination_path_list))
    for cloud_path, local_path in zip(destination_path_list, local_path_list):
        fop.download_file(cloud_path, local_path)
    print()

    # Play downloaded test files
    while True:
        audio_count = input("*How many files to play? (0 .. 3): ")
        if audio_count.isdigit():
            audio_count = int(audio_count)
            if audio_count >=0 and audio_count <= 3:
                for audio in local_path_list[:audio_count]:
                    print(f"Playing {audio}")
                    playsound(audio)
                break
            else:
                print("%s is out of range." % audio_count)
        else:
            print("Invalid input.")
    print()

    # Delete test files in cloud
    while True:
        delete = input("*Delete test files in cloud? (Y/n): ")
        if delete == "Y" or delete == "y":
            for file_path in destination_path_list:
                fop.delete_file(file_path)
            break
        elif delete == "N" or delete == "n":
            break
        else:
            print("Unknown option.")
    print()

    # Delete downloaded files
    while True:
        delete = input("*Delete downloaded files? (Y/n): ")
        if delete == "Y" or delete == "y":
            for file_path in local_path_list:
                os.remove(file_path)
            break
        elif delete == "N" or delete == "n":
            break
        else:
            print("Unknown option.")
    print()


if __name__ == "__main__":
    fop.initialize()
    us223_ct1()
    input("Continue? (Enter): ")
    us223_ct2()
    input("Continue? (Enter): ")
    us223_ct3()
