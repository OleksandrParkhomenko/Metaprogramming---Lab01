ASSIGNMENT_OPS = ("=", "+=", "-=", "*=", "/=")
EQUALITY_OPS = ("==", "!=")
RELATIONAL_OPS = ("<", ">", "<=", ">=")
BITWISE_OPS = ("&", "|", "^")
ADDITIVE_OPS = ("+", "-")
MULTIPLICATIVE_OPS = ("*", "@", "/", "%")


from set_config import set_config
#import re

def fix_spaces(file):
    #pattern = re.compile(r'\s+')

    f = open(file, "r")
    data = f.readlines()
    f.close()
    #tokens = dict()
    config = set_config()
    print(config)

    for index, line in enumerate(data):
        line = list(line)
        for i, elem in enumerate(line):
            if elem is "(" and config["SPACES"]["BEFORE_LEFT_BRACKET"] is True:
                if i > 0 and line[i - 1] != " ":
                    line.insert(i, " ")

            if elem in ASSIGNMENT_OPS and config["SPACES"]["AROUND_ASSIGNMENT_IN_NAMED_PARAMS"]:
                if i > 0 and line[i - 1] != " ":
                    line.insert(i - 1, " ")
                if line[i + 1] != " ":
                    line.insert(i + 1, " ")

        data[index] = line
        #print(line)

    f = open(file, "w")
    for line in data:
        line = "".join(line)
        f.write(line)
    f.close()



