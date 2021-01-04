# rollartBV

## Development version

This program is currently in heavy development. This means that it is not completely functional
and should not be used for production.

The binary executable file is not available currently. See usage section for more information.

## Usage

This program is tested under Ubuntu Linux 20.04 distribution.

### Dependencies

- Python3
- Tkinter for python
- sqlite3 for python (normaly builtin, so you have nothing to install)

```
sudo apt install python3 python3-tk
```

### Generate database

At program starting, database are checked and created if needed. If data structure has changed
with a new version, it will be updated in your current database without the need of any update 
system.

### Start

Go to the extraction forlder and then start rollartBV.py file with python3.

#### Linux

Go to the extraction folder with the following command:

```
cd folder/where/rollartBV/is/saved
```

Execute the following

```
python3 ./rollartBV.py
```
