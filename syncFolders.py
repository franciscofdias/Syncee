""" 
Made by José Francisco Dias

Sync two local folders

"""
import sys
import os
import hashlib
import shutil
import time
import msvcrt
from datetime import datetime

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(origin_folder, destination_folder):
    """
    Syncs the origin folder and the destination folder by copying, updating or
    deleting files

    Parameters
    ----------
    origin_folder (str): The path to the origin folder
    destination_folder (str): The path to the destination folder
    """
    for root, dirs, files in os.walk(origin_folder):
        relative_path = os.path.relpath(root, origin_folder)
        dest_path = os.path.join(destination_folder, relative_path)
        
        # Ensure the nested directory exists in the destination folder
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        # Sync files
        for file_name in files:
            origin_file = os.path.join(root, file_name)
            dest_file = os.path.join(dest_path, file_name)
            
            # Check if the file exists in the destination folder
            if os.path.exists(dest_file):
                # Check if the file has changed
                if md5(origin_file) != md5(dest_file):
                    shutil.copy2(origin_file, dest_file)
                    log_change(f"Updated: {dest_file}")
                    print(f"Updated: {dest_file}")
            else:
                shutil.copy2(origin_file, dest_file)
                log_change(f"Copied: {dest_file}")
                print(f"Copied: {dest_file}")
        
        # Remove files from destination folder that are not in the origin folder
        for file_name in os.listdir(dest_path):
            dest_file = os.path.join(dest_path, file_name)
            origin_file = os.path.join(root, file_name)
            if not os.path.exists(origin_file):
                os.remove(dest_file)
                log_change(f"Deleted: {dest_file}")
                print(f"Deleted: {dest_file}")

def log_change(message):
    """
    Log changes to a log file

    Parameters:
    log_file (str): The path to the log file
    message (str): The message to log
    """
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def main():
    log_change("Started Syncee")

    # Check if the destination folder exists, if not, create it and logs it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        log_change(f"Created destination folder: {destination_folder}")
        print(f"Created destination folder: {destination_folder}")
    
    while True:
        sync_folders(origin_folder, destination_folder)
        time.sleep(time_interval)
        # Check if the user has pressed Enter and if so, terminates
        if msvcrt.kbhit():
            if msvcrt.getwche() == '\r':
                print("Terminated Syncee")
                exit()

if __name__ == "__main__":

    # Check if the command line arguments length is correct
    if len(sys.argv) == 5:
        origin_folder = sys.argv[1]
        destination_folder = sys.argv[2]
        time_interval = int(sys.argv[3])
        log_file = sys.argv[4]
        log_file_splitted = log_file.split('\\')
        destination_folder_splitted = destination_folder.split('\\')
        
        if not os.path.exists(origin_folder):
            print("Origin folder does not exist")
            exit()
        elif origin_folder == destination_folder:
            print("Origin folder and destination folder cannot be the same")
            exit()
        elif log_file_splitted[-2] == destination_folder_splitted[-1]:
            print("Log file cannot be in the same folder as the destination folder")
            exit()
        else:
            print("Starting Syncee")
            print("Press Enter at any time to terminate Syncee at the end of that update cycle")
            main()

    else:
        print(
            "The command must be entered as the following example: 'syncFolders.py' [origin_folder] [destination_folder] [time_interval] [log_file]"
        )
    
