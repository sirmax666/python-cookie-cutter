# Python Cookie Cutter

Cookie Cutter project structure builder for you new repo base on Datahub's
best practices :)

## Usage

```shell
usage: python-cookie-cutter.py [-h] [--init | --newmodule] [--debug]
                               [--silent]
                               LOCATION

positional arguments:
  LOCATION     Output Location without the project name

optional arguments:
  -h, --help   show this help message and exit
  --init       Initialize project
  --newmodule  Initialize a new module (project must have) been initialized
               first
  --debug      Increases verbosity
  --silent     Turns off verbose
```

### Initialize a new project

To create a new project, simply call the script and define a base location
without the name of the project. Let's say you want to create a new project
called `My New Project` in `C:\My Documents\python_projects\`

```shell
python python-cookie-cutter.py "C:\My Documents\python_projects" --init
```

### Initialize a new module

In an existing project, define the root folder of the project. Given the previous
example, this path would be:

`C:\My Documents\python_projects\my_new_project`

```shell
python python-cookie-cutter.py "C:\My Documents\python_projects\my_new_project" --newmodule
```

## Developpers

### Change the structure

Under construction...
