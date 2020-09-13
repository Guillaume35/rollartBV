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
- sqlite3 for python (normaly builtin)

```
sudo apt install python3 python3-tk
```

### Generate database

Installation system is not available. You'll need to create all database by executing each
motors/* python file.

Go to motors/ folder with the following command:

```
cd folder/where/rollartBV/is/saved
```

Execute each python file:

```
python3 element_type.py
python3 element.py
```

### Start

Go to the extraction folder with the following command:

```
cd folder/where/rollartBV/is/saved
```

Execute the following

```
python3 ./rollartBV.py
```
