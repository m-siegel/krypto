"""
    CS 5001, Fall 2021
    Lab 4-B
    Ilana-Mahmea Siegel

    Facilitates a Krypto game/puzzle.

    How krypto works:
    The user is given six distinct random numbers between 1 and 25, inclusive.
    The user comes up with mathematical expressions using arithmetic operators
    and each of the first five numbers, which must evaluate to the sixth
    number.

    This program provides the user with six numbers and evaluates user's
    proposed solutions. When the user enters 'quit', the program prints
    any correct solutions that the user entered.
"""


def main():
    # Print instructions and get optional seed for random number generator
    sd = print_instructions()

    # Run game unless the user wants to quit immediately
    if not (sd == "q" or sd == "quit"):

        # Convert sd to int, if sd exists
        if sd:
            sd = int(sd)

        # Get krypto numbers
        numbers, target = get_numbers(sd)

        # Print numbers for user
        print("\nNumbers: {}, {}, {}, {}, {}.\nTarget: {}"
              .format(numbers[0], numbers[1], numbers[2], numbers[3],
                      numbers[4], target))

        # Get user's solutions and print them (if they exist) when user quits
        solutions = get_solutions(numbers, target)
        if solutions:
            print("\n" + solutions + "Good work!")


def print_instructions():
    """
        Prints Krypto instructions for user and gets optional seed for random
        number generator.

        Return: (string) seed: optional, seed for random number generator
                or quit message.
    """
    print("\nWelcome to the game of Krypto!\n")
    print("Here's how it works:")
    print("I'll give you five random numbers between 1 and 25.")
    print("You need to figure out how to use them to get to"
          " a sixth random number, the 'target.'\n")
    print("You can use multiplication (*), division (/),"
          " addition (+) and subtraction (-).")
    print("You must use all five numbers, and you cannot repeat them.\n")
    print("Enter each solution you think you've come up with.\n")
    print("Enter 'q' or 'quit' at any time to quit.\n")
    print("If you would like to provide a seed for the random numbers, "
          "enter it here.")
    seed = input("Otherwise, just hit 'enter' to start: ")

    return seed


def get_numbers(sd):
    """
        Gets five distinct pseudorandom integers between 1 and 25, inclusive.

        Parameter: (int) sd: optional seed for pseudorandom number generator.
        Return: (ints) num1, num2, num3, num4, num5: distinct random ints.
    """
    numbers = []

    if not sd:
        sd = 7
    num1 = random_int(seed=sd)
    numbers.append(num1)

    # Make sure num2 is distinct from num1
    num2 = num1
    while num2 in numbers:
        num2 = random_int(seed=num2)
    numbers.append(num2)

    # Each number must be distinct from the rest
    num3 = num2
    while num3 in numbers:
        num3 = random_int(seed=num3)
    numbers.append(num3)

    # Each number must be distinct from the rest
    num4 = num3
    while num4 in numbers:
        num4 = random_int(seed=num4)
    numbers.append(num4)

    # Each number must be distinct from the rest
    num5 = num4
    while num5 in numbers:
        num5 = random_int(seed=num5)
    numbers.append(num5)

    # Each number must be distinct from the rest
    target = num5
    while target in numbers:
        target = random_int(seed=target)

    return numbers, target


def get_solutions(numbers, target):
    """
        Prompt user to enter solutions until they enter 'q' or 'quit'.
        Adds valid solutions to string of solutions to return.

        Parameter: (int) target: target number to send to valid_solution()
        Return: (str) solutions: each valid solution the user entered
    """

    # Initialize solutions string so it persists after loop
    solutions = ""

    # Get first attempted solution to use as loop condition
    attempt = input("\nEnter solution: ")

    # Get and check attempted solutions until user quits
    while not (attempt == "q" or attempt == "quit"):

        # Add valid solutions
        if valid_solution(attempt, numbers, target):

            if solutions:

                # Tack new solutions onto end of solutions string
                solutions += attempt + "=" + target + "\n"
            else:
                # Wait to add header until there's one solution so solutions
                # can be empty if no valid solution has been entered.
                solutions += "Your solutions:\n{} = {}\n".format(attempt,
                                                                 target)
        else:
            # Spacial message if solution fails
            print("Try again.\n")

        # Next attempt
        attempt = input("Enter solution: ")

    # Contains all of user's correct solutions. Empty if no solutions entered.
    return solutions


def valid_solution(attempt, numbers, target):
    """
        Validates that expression evaluates to target value.

        Parameters:
            (string) attempt: mathematical expression to be converted to list
            (list) numbers: ints that can appear in mathematical expression
            (int) target: number that mathematical expression should eval to

        Return:
            (bool): False if format or elements of attempt are invalid for
                    given krypto puzzle or if expression doesn't evaluate
                    to target. Otherwise True.

        Side effects: prints messages to user about success or failure of
                      attempt.
    """

    # Get string attempt as a list of numbers and operations as strings
    expression = get_list_expression(attempt, numbers)
    # If get_list_expression found issues with attempt, return False
    if not expression:
        return False

    # Get value of expression, or False if something's wrong with exp syntax
    value = evaluate_expression(expression)
    if not value:
        return False

    # Confirm expression evaluates to target number
    if value == target:
        print("Krypto!")
        return True
    else:
        print("Evaluates to {}, not {}.".format(value, target))
        return False


def get_list_expression(attempt, numbers):
    """
        Converts string mathematical expression into a list of all elements
        of given expression.

        Returns False if attempt uses any numbers that aren't in numbers
        list or if attempt uses operations that aren't in hard-coded
        list (["*", "/", "+", "-"]).

        Parameter: (str) attempt: Mathematical expression with integers,
            +, -, *, /, (, ), or spaces.
        Parameter: (int) target: Integer that attempt should evaluate to.

        Return: (list) expression or (bool): list strings representing
                numbers and operations from input string. Returns False if
                a number in attempt is not in parameter numbers, if any
                characters aren't numbers or in list of approved symbols,
                or if there's the wrong number of operations.
    """

    # To count operations in attempt. There should be 4 (for 5 numbers)
    ops = 0

    # To hold each operand and operation in attempt
    expression = []

    # To store 2-digit numbers as iterating over string, one char at a time
    current_num_string = ""

    # Iterate over string to separate operands and operations instead of
    # using .split() in case user leaves out spaces
    for character in attempt:

        # Temporarily store digits in current_num_string for 2-digit numbers
        if character.isnumeric():
            current_num_string += character

        else:

            # If last number has ended and hasn't been appended to expression
            if current_num_string:

                # Confirm current number is one of the given numbers
                if int(current_num_string) not in numbers:
                    print(current_num_string,
                          "isn't one of the given numbers.", end=' ')
                    return False

                else:
                    # Add to expression list
                    expression.append(current_num_string)
                    current_num_string = ""

            # Add valid operations to expression list
            if character in ["*", "/", "+", "-"]:
                expression.append(character)

                # Count operations to confirm correct number
                ops += 1

            # Not operations, but valid symbols to include
            elif character in ["(", ")"]:
                expression.append(character)
            elif character == " ":
                continue

            # Anything else is an invalid symbols
            else:
                print("'" + character + "' is an invalid symbol.", end=' ')
                return False

    # Need to append last number to list
    # Confirm current number is one of the given numbers
    if current_num_string:
        if int(current_num_string) not in numbers:
            print(current_num_string,
                  "isn't one of the given numbers.", end=' ')
            return False
        else:
            # Add to expression list
            expression.append(current_num_string)

    # Confirm correct number of operations (and numbers, by extension)
    if ops != 4:
        print("Incorrect number of operations.", end=' ')
        return False

    return expression


def evaluate_expression(expression):
    """
        Evaluate mathematical expression, represented by expression string.

        Parameter: (list) expression: mathematical expression. Each element
                    is a string: integer, arithmetic operation or parentheses.

        Return: (int) value or (bool) False: value of expression or False
                if missing a close-parentheses.
    """

    # Running value of expression
    value = 0

    # The next operand and operation to perform
    next_operand = 0
    next_operation = ""

    # Use a while loop so can conditionally change i's value as needed
    i = 0
    while i < len(expression):

        # Get numbers as operands
        if expression[i].isnumeric():
            if not value:
                value = int(expression[i])
            else:
                next_operand = int(expression[i])

        # Get operation to perform
        elif expression[i] in ["*", "/", "+", "-"]:
            next_operation = expression[i]

        # Parentheses --
        # Evaluate expression inside parentheses before proceeding
        elif expression[i] == "(":

            # Search for index of corresponding close-parenthesis
            j = i + 1
            extra_parens = 0
            while expression[j] != ")" or extra_parens:
                if expression[j] == "(":
                    extra_parens += 1
                elif expression[j] == ")":
                    extra_parens -= 1
                j += 1

                # In case user didn't enter corresponding close-parenthesis,
                # Don't index beyond end of list
                if j == len(expression):
                    print("Missing close-parenthesis.", end=' ')
                    return False

            # Evaluate expression inside parentheses to be next operand
            # Recursive
            next_operand = evaluate_expression(expression[(i + 1):j])

            # skip to other side of parentheses after evaluating val inside
            i = j

        # Evaluate new value based on next_operand and next_operation
        if next_operand and next_operation:
            value = operate(value, next_operation, next_operand)

            # Reset next_operand and next_operation so don't enter this block
            # without getting a new next_operand and new next_operation.
            next_operand = 0
            next_operation = ""

        # Increment i to iterate through list
        i += 1

    return value


def random_int(seed=7, max_num=25):
    """
        Returns a pseudorandom integer between 1 and max_num, inclusive.

        Note: Written for a class before we've learned about the time library.
              A better default seed would be int((time.time() % 1) * 100)

        Parameters:
        (int) seed: seed for random number generation
        (int) max_num: maximum number that can be returned

        Returns:
        (int) num: pseudorandom number
    """

    # Generate pseudorandom number.
    # Multiply seed by prime so generated numbers will work their way through
    # all ints between 1 and max_num
    # Add 1 after mod to shift range from [0 to (max_num - 1)]
    # to [1 to max_num]
    num = ((17 * seed + 1) % max_num) + 1
    return num


def operate(operand_1, operation, operand_2):
    """
        Performs given mathematical operation on given operands.

        Parameters:
            (int or float) operand_1: first operand
            (string) operation: operation to perform
            (int or float) operand_2: second operand

        Return: (int or float): result of performing operation
    """
    # QUESTION: Is it better to have many possible returns like this or to
    # do value *= next_operand, etc. and then return value at the end?
    if operation == "*":
        return operand_1 * operand_2
    if operation == "/":
        return operand_1 / operand_2
    if operation == "+":
        return operand_1 + operand_2
    if operation == "-":
        return operand_1 - operand_2


if __name__ == "__main__":
    main()
