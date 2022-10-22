from genericpath import isfile
import os
import test

def list_of_local_files(path:str):
    os.chdir(path)
    files = []
    for dir in sorted(os.listdir(),reverse=True):
        if os.path.isdir(dir):
            files = files + [path+"/"+file for file in list_of_local_files(dir)]
        if os.path.isfile(dir):
            files.append(path+"/"+dir)
    os.chdir("..")
    return files

if __name__ == "__main__":
    test.initialize()

    list(map(print, test.list_files()))

    # Download
    # for file in test.list_files():
    #     test.download_file(file, file)

    #Upload
    for file in list_of_local_files("./Users"):
        d_file = file.lstrip(".")
        test.upload_file(file)
    
    # test.list_files()
