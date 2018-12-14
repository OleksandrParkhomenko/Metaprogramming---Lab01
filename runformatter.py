import sys
from formatter import format

if len(sys.argv) < 2:
    print("Error! Expected name of file.")
else:
    if "-h" in sys.argv[1:]:
        print("""To format your Python code use commands described bellow:\n
        python runformatter.py <name of file to format> 
            | format your file with default configurations\n
        python runformatter.py <name of file to format> -f <configuration file>
            | format with configs in chosen file\n
        python runformatter.py <name of file to format> -c <option of config-1><value-1>...<option of config-N><value-N>
            |format with default but some options is changing\n
        python runformatter.py <name of file to format> -c <option of config-1><value-1>...<option of config-N><value-N> -n <file to save configs> 
            |format with default but some options is changing and save them to another file 
         """)
    else:
        try:

            format(sys.argv)
        except OSError:
            print("Error! File not found.")

