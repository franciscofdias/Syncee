# Syncee

## About the program

This Python project goal is to synchronize a given local folder with another local folder making it a replica, updating from a given time to time and writes the operations in a log file.

## Running

To run the program, it must be given 4 arguments: a string containing the source folder location; a string containing the destination folder location; a int seconds in which the folder is updated; a string containing the destination of the logfile.txt.

```
py syncFolder.py <source_folder_location> <destination_folder_location> <time_in_seconds> <Logfile.txt_location>
```
