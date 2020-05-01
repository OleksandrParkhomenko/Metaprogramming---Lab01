def set_config(argv=[], new_config="", config_to_use=""):
    import re
    pattern = re.compile(r'\s+')

    interactive = "-i" in argv
    answer = True
    if interactive:
        print("Welcome to interactive mode of setting formatting configurations!")
        if config_to_use != "":
            print(config_to_use, "is used as a template.")
        else:
            print("Default template is used.")

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
                value = line[pos + 1:]

                if interactive and answer:
                    print(key, "|Default:", value)
                    new_value = input("New value:")
                    if new_value != "":
                        value = new_value

                if value == "False":
                    value = False
                elif value == "True":
                    value = True
                else:
                    value = int(value)

                config[curr_section][key] = value
            else:
                curr_section = line
                while interactive and True:
                    print("Do you want to change anything in category", curr_section, "? y/n")
                    _answer = input()
                    if _answer.lower() == 'y':
                        answer = True
                        print("For each option enter new value or press \'Enter\' to skip and set default.")
                        break
                    elif _answer.lower() == 'n':
                        answer = False
                        break
                    else:
                        print("Wrong answer! y/n")

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

    if interactive:
        new_config = input("Enter new config file name:")

    if new_config != "":
        f = open(new_config, "w")
        for section in config:
            f.write(section + "\n")
            for option in config[section].keys():
                f.write("\t" + option + "=" + str(config[section][option]) + "\n")
        f.close()
        print("NEW CONFIGURATION FILE CREATED")

    return config

# set_config()
# set_config(["indent", "5", "BEFORE_LEFT_BRACKET", "true"],new_config="new_config.txt")
# set_config(config_to_use="new_config.txt")
