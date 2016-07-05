# Associate *.jff files with JFlapToCode

## Windows:

Run the following commands on the windows command line as an administrator:

assoc .jff=JFlapFile

ftype JFlapFile="**PYTHON_EXE_PATH**\python.exe" "**JFlapToCode_Dir**\JFlapToCode.py" "%1" %*

**PYTHON_EXE_PATH** is the directory on your machine where python is installed

**JFlapToCode_Dir** is the directory on your machine where this repo has been cloned
