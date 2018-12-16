# Python Code Formatter
>Metaprogramming | Lab 01 


Develop a console interactive formatting utility (positional tabulation) for Python 3.x Coding. The system should interact with the user through the console interface and take:
1. Analyze the structure of Python files and detect irregularities and the positioning of structural elements of documents and structural errors in their codes. In the case of structural discoveries errors, the system should display messages about found errors and perform formatting of Python documents with their account. The error message should be posted the error text and the number of the corresponding line.

2. To format the placement of the structural elements of the input Python files using a definite Python-formatting format template. In the quality of the basic format for formatting Python files need to use [PyCharm 2018.2 Code Style. Python](https://www.jetbrains.com/help/pycharm/code-style-python.html)
3. Create and edit your own templates for Python code formatting. Realize individual commands for performing various system functions. Utility should be started from command line of the operating system terminal. For demonstration of system operation it is necessary to use Python files from GitHub or GitLab.





### To format your Python code use commands described bellow:
Get help using:
```sh 
$ python runformatter.py -h
```

Formatting your file with default configurations:
```sh 
$ python runformatter.py <name of file to format> 
```
Formatings with configurations from chosen file:
```sh
$ python runformatter.py <name of file to format> -f <configuration file>
```          
Formatting with default configuration but given options is changed:
```sh
$ python runformatter.py <name of file to format> -c <option of config-1><value-1>...<option of config-N><value-N>
```
Formatting with default configuration, given options is changed and saved as another configuration file:
```sh
$ python runformatter.py <name of file to format> -c <option of config-1><value-1>...<option of config-N><value-N> -n <file to save configs> 
```
Run interactive mode for creation your own customized configuration template:
```sh
$ python runformatter.py -i
```
Run interactive mode for creation your own customized configuration template based on configuration file you entered:
```sh
$ python runformatter.py -i -f <configuration file>
```




