string = "1234567890"
x_min = 4
y_max = 8


def to_dict(string):
    dict = {}
    old_i = string[-1]
    for i in string:
        dict[old_i] = i
        old_i = i
    return dict


def is_correct_password(password):
    # Placeholder function: replace with your actual password validation function
    # Return True if the password is correct, otherwise False
    return password == "9043433"


dict = to_dict(string)
end = string[-1]

for length in range(x_min, y_max + 1):
    x = [string[0]] * length  # Initialize x with the current length
    attempts = 0
    max_attempts = len(string) ** length  # Calculate the maximum number of attempts

    while attempts < max_attempts:
        password = "".join(x)
        if is_correct_password(password):
            print(f"Correct password found: {password}")
            break

        for i in range(len(x)):
            if x[i] != end:
                x[i] = dict[x[i]]
                break
            else:
                x[i] = string[0]
                if i == len(x) - 1:
                    x.append(string[0])
                    if len(x) > length:
                        x = [
                            string[0]
                        ] * length  # Reset x if it exceeds the current length
                        break

        attempts += 1
    else:
        continue
    break
else:
    raise ValueError(
        "All possible passwords have been exhausted without finding the correct password."
    )
