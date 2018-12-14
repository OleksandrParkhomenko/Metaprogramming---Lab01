

def set_config(argv=[], new_config="", config_to_use=""):

    import re
    pattern = re.compile(r'\s+')

    if config_to_use == "":
        f = open(r"config.txt", "r")
    else:
        try:
            f = open(config_to_use, "r")
        except OSError:
            print("CONFIGURATION FILE NOT FOUND!\nDEFAULT CONFIGURATION WILL BE USED")
            f = open(r"config.txt", "r")
    data = f.readlines()
    config = dict()

    for line in data:
        line = re.sub(pattern, '', line)
        if line != '':
            pos = line.find('=')
            if pos != -1:
                key = line[:pos]
                value = line[pos+1:]
                if value == "False":
                    value = False
                elif value == "True":
                    value = True
                else:
                    value = int(value)

                config[curr_section][key] = value
            else:
                curr_section = line
                config[curr_section] = dict()

    for i, key in enumerate(argv[:-1]):
        if i % 2 == 0:
            value = argv[i + 1]
            key = key.upper()

            for section in config.keys():
                if key in config[section].keys():
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    else:
                        value = int(value)
                    config[section][key] = value

    if __name__ == '__main__':
        print(config)

    if new_config != "":
        f = open(new_config, "w")
        for section in config:
            f.write(section + "\n")
            for option in config[section].keys():
                f.write("\t" + option + "=" + str(config[section][option]) + "\n")
        f.close()
        print("NEW CONFIGURATION FILE CREATED")

    return config


#set_config()
#set_config(["indent", "5", "BEFORE_LEFT_BRACKET", "true"],new_config="new_config.txt")
#set_config(config_to_use="new_config.txt")