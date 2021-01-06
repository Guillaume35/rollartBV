# Rollart Unchained

## Development version

This program is currently in heavy development. This means that it is not completely functional
and should not be used for production.

The binary executable file is not available currently. See usage section for more information.

## Usage and installation

This program is currently tested under Ubuntu Linux 20.04 distribution and Windows 10 system.

No standalone package is still ready. It needs manual installation of the following dependencies :

- Python3
- Tkinter for python (normaly builtin since python 3, so you have nothing more to install)
- sqlite3 for python (normaly builtin, so you have nothing to install)

### Linux

Install python3 from official distribution repository.

```
sudo apt install python3 python3-tk
```

### Windows

Install python3 from official website. Be sure you download the last stable version 3.

https://www.python.org/downloads/windows/

## Start application

Once all dependencies are installed, go to the extraction forlder and then start rollartBV.py file 
with python3.

### Linux

Go to the extraction folder with the following command:

```
cd folder/where/rollartBV/is/saved
```

Execute the following

```
python3 ./rollartBV.py
```

### Windows

Type **Win + R** and enter *cmd* to start command line program.

In the command line, start rollartBV.py with python3 :

```
py path\to\rollartBV.py
```

## Datas

At program starting, database are checked and created if needed. If data structure has changed
with a new version, it will be updated in your current database without the need of any update 
system.

All application data are saved in a .rollartBV/ folder located in the home directory. The location 
of this directory can vary, depending on your system and configuration.

### Linux

Date folder should be the following :
*/home/YOU/.rollartBV*

### Windows

Data folder should be the following :
*C:\Users\YOU\.rollartBV*

## Contribute

This is an open source project. You can contribute in many ways :

### Development

If you have skills in development, you can fork this program and propose changes and improvments in
the code.

### System test, report technical issues

You are invited to test the application on different platforms : Windows, Linux, Mac OS... and report 
any troubles in the execution of the program.

Register GitHub and use Issues tab to report any issue.

### Judgment test, report calculating issues

For judges, data operators, specialists, you are invited to test the application and report any issues 
that can cause bad calculating or bad ranking for a program.

Calculating issues are concidered with a high priority level for fixing them.

Register GitHub and use Issues tab to report any issue.

### Documentation

You are invited to document the program in any languages you want so it will be easier to use it. The
documentation can be propose in the wiki page.

### Request new functions

If you are not a developper but you want new functions in the application, you can just ask for them.

Register GitHub and use Issues tab to report any proposal.
