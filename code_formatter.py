
def clean_add_spaces(line, tabs):
    start = True
    num_spaces = 0
    i = 0
    for _char in line:
        # _char = line[i]
        if (_char == ' ') and start:
            num_spaces += 1
            if num_spaces > 4 * tabs:
                buff = line.replace(_char, '', 1)
                line = buff
        elif _char in {'+', '-', '*', '/', '=', ','}:
            if i != 0 and line[i - 1] != ' ' and _char != ',':
                line = line.replace(line[i - 1], line[i - 1] + ' ')
            elif line[i + 1] != ' ':
                line = line.replace(line[i + 1], ' ' + line[i + 1])
        # elif (_char == ' ') and not start:
        # if i > 0:
        # if line[i-1] == ' ':
        #   line = line.replace(line[i-1], '')
        else:
            start = False
        i += 1
    if num_spaces < 4 * tabs:
        line = ' ' * (4 * tabs - num_spaces) + line

    return line


file = open("file01.py", "r")
data = file.readlines()
file.close()
tab = 0
for i in range(len(data)):
    buff = clean_add_spaces(data[i], tab)
    data[i] = buff
    if data[i].find("def") != -1:
        tab += 1
    elif tab > 0:
        tab -= 1

file = open("file01.py", "w")
file.writelines(data)
file.close()
