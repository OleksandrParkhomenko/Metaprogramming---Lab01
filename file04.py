values = ["True", "False"]

print("For each option enter new value or press \'Enter\' to skip and set default.")
for i, item in enumerate(values):
    print("BLANK_LINES MAX_IN_CODE |Default:", item, "|")
    new_value = input()
    if new_value != "":
        values[i] = new_value

print(values)
