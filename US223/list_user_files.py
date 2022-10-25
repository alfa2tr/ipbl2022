import os

def undo_dir_changes(func):
    def inner(path:str):
        start_path = os.getcwd()
        list_of_paths = func(path)
        os.chdir(start_path)

        return list_of_paths
    return inner

@undo_dir_changes
def list_of_local_files(path:str):
    os.chdir(path)
    files = []
    for dir in sorted(os.listdir(),reverse=True):
        if os.path.isdir(dir):
            files = files + [path+"/"+file for file in list_of_local_files(dir)]
        if os.path.isfile(dir):
            files.append(path+"/"+dir)
    #os.chdir("..")
    return files

def get_file_name_from_path(path: str) -> str:
    return path.split("/")[-1]

if __name__ == "__main__":
    print("Current folder: %s" % os.getcwd().split("/")[-1])
    list(map(print, list_of_local_files("US223/Users")))
    print("Current folder: %s" % os.getcwd().split("/")[-1])
