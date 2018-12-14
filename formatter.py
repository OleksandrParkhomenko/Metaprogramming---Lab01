import string
from keyword import kwlist

ASSIGNMENT_OPS = ("=", "+=", "-=", "*=", "/=")
EQUALITY_OPS = ("==", "!=")
RELATIONAL_OPS = ("<", ">", "<=", ">=")
BITWISE_OPS = ("&", "|", "^")
ADDITIVE_OPS = ("+", "-")
MULTIPLICATIVE_OPS = ("*", "@", "/", "%")
SHIFT_OPS = ("<<", ">>", ">>>")
POWER_OP = "**"


def split(data, config):
    indent_levels = list()
    for index, line in enumerate(data):
        line = list(line)
        i = 0
        spaces_on_begin = 0
        begin = True
        while i < len(line):
            if begin and line[i] == " ":
                spaces_on_begin += 1
            else:
                begin = False

            if line[i] in string.punctuation and line[i] != "." and line[i] != "_":
                if line[i] == line[i+1] or (line[i]+line[i+1] in (EQUALITY_OPS + ASSIGNMENT_OPS)):
                    line.insert(i + 2, " ")
                    line.insert(i, " ")
                    i += 3
                else:
                    line.insert(i + 1, " ")
                    line.insert(i, " ")
                    i += 2
            i += 1
        line = "".join(line)
        line = line.split()
        data[index] = line
        indent = int(spaces_on_begin / config["TABS_AND_INDENTS"]["INDENT"])
        if not indent_levels:
            indent_levels.append(0)
        elif indent_levels[-1] < indent:
            indent_levels.append(indent_levels[-1] + 1)
        else:
            indent_levels.append(indent)

    return data, indent_levels


def tokenize(data, config):
    data, indent_levels = split(data, config)
    tokens = list(dict())
    for line in data:
        for item in line:
            if item in kwlist:
                item = (item, "KEYWORD")
            elif item in string.punctuation+"<<>><<<**==":
                item = (item, "PUNCTUATION")
            else:
                item = (item, "NAME or VALUE")
            tokens.append(item)
        tokens.append(("\n", "NEW_LINE"))

    return tokens, indent_levels


def refact(tokens, indent_levels, config):
    data = list()
    line = ""

    __func_names = list()
    __method_declaration = False
    __method_call = False
    __indent = 0
    __continuation_indent = False
    __line_num = 0
    __blank_lines = -1

    for i, item in enumerate(tokens):
        __after = False
        __before = False
        __within = False
        __around = False

        #func_names = list()
        token_type = item[1]
        token = item[0]

        if token in ("def", "for", "if", "elif", "else", "try", "class", "while"):
            __indent += 1

        if token_type == "KEYWORD":
            if token == "def":
                __method_declaration = True
                __func_names.append(tokens[i + 1][0])
            __after = True
            if line != "":
                __before = True
        elif token_type == "PUNCTUATION":
            if token == "(":
                if __method_declaration:
                    if tokens[i + 1][0] == ")" and config["SPACES"]["WITHIN_EMPTY_METHOD_DECLARATION_PARENTHESES"]:
                        __within = True
                    elif tokens[i + 1][0] != ")" and config["SPACES"]["WITHIN_METHOD_DECLARATION_PARENTHESES"]:
                        __within = True
                    if config["SPACES"]["BEFORE_PARENTHESES_METHOD_DECLARATION"]:
                        __before = True
                elif __method_call:
                    if tokens[i + 1][0] == ")" and config["SPACES"]["WITHIN_EMPTY_METHOD_CALL_PARENTHESES"]:
                        __within = True
                    elif config["SPACES"]["WITHIN_METHOD_CALL_PARENTHESES"]:
                        __within = True
                    if config["SPACES"]["BEFORE_PARENTHESES_METHOD_CALL"]:
                        __before = True
            elif token == ")":
                if __method_call:
                    if config["SPACES"]["WITHIN_METHOD_CALL_PARENTHESES"] and tokens[i - 1][0] != "(":
                        __before = True
                    __method_call = False
                if __method_declaration and\
                        config["SPACES"]["WITHIN_METHOD_DECLARATION_PARENTHESES"] and tokens[i - 1][0] != "(":
                    __before = True
            elif token == POWER_OP and config["SPACES"]["AROUND_POWER_OP"]:
                __around = True
            elif token in SHIFT_OPS and config["SPACES"]["AROUND_SHIFT_OPS"]:
                __around = True
            elif token in ASSIGNMENT_OPS:
                if __method_declaration and config["SPACES"]["AROUND_ASSIGNMENT_IN_NAMED_PARAMS"]:
                    __around = True
                elif __method_call and config["SPACES"]["AROUND_ASSIGNMENT_IN_KEYWORD_ARGS"]:
                    __around = True
                elif not __method_declaration and not __method_call and config["SPACES"]["AROUND_ASSIGNMENT_OPS"]:
                    __around = True
            elif token in EQUALITY_OPS and config["SPACES"]["AROUND_EQUALITY_OPS"]:
                __around = True
            elif token in RELATIONAL_OPS and config["SPACES"]["AROUND_RELATIONAL_OPS"]:
                __around = True
            elif token in BITWISE_OPS and config["SPACES"]["AROUND_BITWISE_OPS"]:
                __around = True
            elif token in ADDITIVE_OPS and config["SPACES"]["AROUND_ADDITIVE_OPS"]:
                __around = True
            elif token in MULTIPLICATIVE_OPS and config["SPACES"]["AROUND_MULTIPLICATIVE_OPS"]:
                __around = True

            elif token == "[":
                if config["SPACES"]["BEFORE_LEFT_BRACKET"]:
                    __before = True
                if config["SPACES"]["WITHIN_BRACKETS"]:
                        __within = True
            elif token == "{" and config["SPACES"]["WITHIN_BRACES"]:
                __within = True
            elif token == ",":
                if config["SPACES"]["BEFORE_COMA"]:
                    __before = True
                if config["SPACES"]["AFTER_COMA"]:
                    __after = True
            elif token == ":":
                if config["SPACES"]["BEFORE_COLON"]:
                    __before = True
                if config["SPACES"]["AFTER_COLON"]:
                    __after = True
                if __method_declaration:
                    __method_declaration = False
            elif token == "\\":
                if config["SPACES"]["BEFORE_SLASH"]:
                    __before = True
            elif token == "#":
                if config["SPACES"]["BEFORE_SHARP"]:
                    __before = True
                if config["SPACES"]["AFTER_SHARP"]:
                    __after = True
            elif token == ";" and config["SPACES"]["BEFORE_FOR_SEMICOLON"]:
                __before = True
        elif token_type == "NAME or VALUE":
            if not __method_declaration and token in __func_names:
                __method_call = True

            if tokens[i + 1][0] != "," and not __after and not (__method_call or __method_declaration):
                __after = True

        if __around:
            if line[-1:] != " ":
                line += " "
            line += token + " "
        else:
            if __before and line[-1:] != " ":
                line += " "
            elif not __before and line[-1:] == " " and tokens[i - 1][1] == "NAME or VALUE":
                line = line[:-1]
            line += token
            if __after or __within:
                line += " "

        __class_or_func = indent_levels[__line_num] < indent_levels[__line_num-1] or __blank_lines > -1

        if token_type == "NEW_LINE":
            __blank_lines += 1
            if (__class_or_func and __blank_lines <= config["BLANK_LINES"]["AROUND_TOP_LEVEL_CLASSES_AND_FUNCS"])\
                    or (__blank_lines <= config["BLANK_LINES"]["MAX_IN_CODE"])\
                    or (__method_declaration and __blank_lines < config["BLANK_LINES"]["MAX_IN_DECLARATION"]):
                data.append(line)
                __line_num += 1
                line = ""
            else:
                line = ""

            if i < len(tokens) - 1:
                line += " " * indent_levels[__line_num] * config["TABS_AND_INDENTS"]["INDENT"]
        else:

            __blank_lines = -1




    return data


def format(argv):
    try:
        file = argv[1]
        f = open(file, "r")
    except OSError:
        print("Error! File not found.")
    else:
        args = []
        new_config = ""
        config_to_use = ""
        if len(argv) > 2 and argv[2] == "-c":
            if "-n" in argv:
                args = argv[3:argv.index("-n")]
                new_config = argv[argv.index("-n") + 1]
            else:
                args = argv[3:]
                new_config = ""
        elif len(argv) > 2 and argv[2] == "-f":
            config_to_use = argv[argv.index("-f") + 1]

        from set_config import set_config
        config = set_config(args, new_config, config_to_use)
        tokens, indent_levels = tokenize(f.readlines(), config)
        data = refact(tokens, indent_levels, config)
        f.close()
        f = open(file, "w")
        f.writelines(data)
        f.close()
