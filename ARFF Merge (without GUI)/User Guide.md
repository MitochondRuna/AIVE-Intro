# .arff file merger User Guide

## Windows (with .exe Application only)

1. Drag (Move) all your .arff file to the same folder as the application.
2. Double click the application to merge.
3. You will see a log file which named the time you started merging and (ideally) the final output in the same folder.
4. If only a log file is generated, follow the log file's report and check the file which led to the termination.

## Windows (with code)

1. Make sure packages are all equipped (os, glob, datetime & pyinstaller).
2. After modifying the code (Thanks!), Drag (Move) all your .arff file to the same folder as the application, then just run the code.
3. If want to generate a application, follow the command: `pyinstaller --onefile YourFileName.py` then operate as the description above.

## Linux

1. Make sure Python is installed in the Linux device & packages are all equipped (os, glob, datetime & pyinstaller).
2. After modifying the code (Thanks!), Drag (Move) all your .arff file to the same folder as the application, then just run the code.
3. If want to generate a application, follow the command: `pyinstaller --onefile YourFileName.py` then operate as the description above.
4. If your Linux system have a GUI, you can just launchthe merging by clicking as the Windows, if not, go to the application's folder, check that all the file is ready, then typing `./YourApplicationName`  in the command line to launch.