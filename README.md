# GCT-memory-aware-PL-project
This repository presents our work on the PL class subproject 1, memory-aware aspect.

# HOW TO CREATE VARIABLES ENVIRONMENT IN:

## WINDOWS
open *cmd* from Windows icon on keyboard

* check if you have python
> python3 --version

(to install python):
> sudo apt install python3

* check if venv is installed first:
> python -m venv --help

_se supone que le sale muchos comandos en forma de menu, asi se confirma que si esta instalado_

_si no le sale nada o le sale error de algun tipo_

in the case that it is NOT installed:
> sudo apt-get install python3-venv

* navigate to your project directory (folder donde quieres guardar el venv):
> cd path/to/your/project

* to create the virtual venv:
> python -m venv *venv_name*

to list the files in the folder type below command in the terminal:
> dir *venv_name*

to activate the variable environment:
> \path\to\venv\Scripts\activate

change Directory to Scripts:
> cd venv\Scripts

activate the Virtual Environment:
> activate.bat

Install Packages:
> pip install requests

## MACOS/LINUX
open *Terminal* or *Bash* from Windows icon on keyboard

* check if you have python
> python3 --version

(to install python):
> sudo apt install python3

* check if venv is installed first:
> python -m venv --help

_se supone que le sale muchos comandos en forma de menu, asi se confirma que si esta instalado_

_si no le sale nada o le sale error de algun tipo_

in the case that it is NOT installed:
> sudo apt-get install python3-venv

* navigate to your project directory (folder donde quieres guardar el venv):
> cd path/to/your/project

* to create the virtual venv:
> python -m venv *venv_name*

to list the files in the folder type below command in the terminal:
> dir *venv_name*

to activate the variable environment:
> source path/to/venv/bin/activate

change Directory to Scripts:
> cd venv\Scripts

activate the Virtual Environment:
> activate.bat

Install Packages:
> pip install requests

## AFTER SETTING VENV
1. open venv folder in VScode and open the Command Palette, there select:
> Git: Clone

2. and using the URL from Github, copy it there and select the venv as the location folder

3. open venv folder, now with project folder inside of it, in VScode

4. open VScode terminal and repeat the activate step depending on your OS and it should show the follow:
> (*venv_name*) PS C:\path\to\your\project> 

5. now you're ready to start coding on the project! good work!