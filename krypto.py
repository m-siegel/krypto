"""
    Created by I-M Siegel
    Updated 10-8-21

    Facilitates a Krypto game/puzzle.

    How krypto works:
    The user is given six distinct random numbers between 1 and 25, inclusive.
    The user comes up with mathematical expressions using arithmetic operators
    and each of the first five numbers, which must evaluate to the sixth
    number.

    This program provides the user with six numbers and evaluates user's
    proposed solutions. When the user enters 'quit', the program prints
    any correct solutions that the user entered.

    The program takes an optional seed for its random number generator.

    When evaluating mathematical expressions, the program ignores normal order
    of operations. It evaluates expressions from left to right, except where
    parentheses indicate otherwise.

    Accepted mathematical operations are multiplication (*), division (/),
    addition (+), subtraction (-), factorial (!), exponent (^) and root (v).
    Note: for radical operations, the index must come after the radicand
    (sqrt(x) is written as x v 2).

    --------------------------------------------------------------------------

    NOTE: This program intentionally does not import other Python libraries to
    help with evaluating the mathematical operations or obtaining random
    numbers. This means that the pseudorandom number generator in particular
    isn't that random because it can't incorporate some variable element, like
    time, into how it selects numbers.

    --------------------------------------------------------------------------

    EXAMPLE RUN:
    To distinguish user input from output, input is in single quotes here.

    If you would like to provide a seed for the random numbers,
    enter it here.
    Otherwise, just hit 'enter' to start: '4'

    Numbers: 20, 17, 16, 24, 10.
    Target: 22

    Enter solution: '17 + 24 / (16 v (20 /10))'
    Evaluates to 10.25, not 22.
    Try again.

    Numbers: 20, 17, 16, 24, 10.
    Target: 22
    Enter solution: '17 + (24 / (16 v (20 /10)))'
    One off!

    Numbers: 20, 17, 16, 24, 10.
    Target: 22
    Enter solution: '20 / (24 + 16 / 10) + 17'
    Krypto!

    Numbers: 20, 17, 16, 24, 10.
    Target: 22
    Enter solution: 'q'

    Your solutions:
    One off:  17 + (24 / (16 v (20 /10))) = 23
    Krypto: 20 / (24 + 16 / 10) + 17 = 22
    Good work!
"""

# Acceptable operators
ACCEPTED_OPERATORS = ["*", "/", "+", "-", "!", "^", "v"]


def main():
    """
        Prints instructions.
        If user doesn't enter quit code, gets and prints pseudorandom numbers,
        then starts accepting user answers.
        Once user enters quit code, prints user's solutions and
        'Good Work! message.
    """
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
        print_numbers(numbers, target)

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
          " a sixth random number,\nthe 'target.'\n")
    print("You can use multiplication, division, addition, subtraction,\n"
          "exponentiation, radicals, and factorials:\n")
    print_operator_key()
    print("NOTE: PROGRAM DOES NOT RECOGNIZE NORMAL ORDER OF OPERATIONS:\n"
          "      Operations proceed from left to right, except where\n"
          "      parentheses indicate otherwise.\n")
    print("You must use all five numbers, and you cannot repeat them.\n")
    print("Enter each solution you think you've come up with.")
    print("Solutions that are 1-off from the target are okay, too.\n")
    print("Enter 'q' or 'quit' at any time to quit.\n")
    print("If you would like to provide a seed for the random numbers,\n"
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


def print_numbers(numbers, target):
    """
        Prints elements 0-4 from numbers and prints target.

        Input:
            (list) numbers: list of 5 operand numbers.
            (int) target: target number
    """

    print("\nNumbers: {}, {}, {}, {}, {}.\nTarget: {}"
          .format(numbers[0], numbers[1], numbers[2], numbers[3], numbers[4],
                  target))


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

        # Add valid solutions (offset from target by no more than 1)
        offset = valid_solution(attempt, numbers, target)
        if offset in [-1, 0, 1]:

            # label solutions as one off or krypto for later printing
            label = "One off: " if offset else "Krypto:"

            if not solutions:
                # Wait to add header until there's one solution so solutions
                # can be empty if no valid solution has been entered.
                solutions += "Your solutions:\n"
            # Tack new solutions onto end of solutions string
            solutions += "{} {} = {}\n".format(label, attempt,
                                               target + offset)

        else:
            # Spacial message if solution fails
            print("Try again.")

        # Next attempt
        print_numbers(numbers, target)
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
            (int or float): 0 if expression evaluates to target
                            +1 if expression evaluates to one greater,
                            -1 if expression evaluates to one less.
                            float('inf') as error value if format or elements
                            of attempt are invalid for given krypto puzzle,
                            or if expression doesn't evaluate to target or
                            one off.

        Side effects: prints messages to user about success or failure of
                      attempt.
    """

    # Get string attempt as a list of numbers and operations as strings
    expression = get_list_expression(attempt, numbers)
    # If get_list_expression found issues with attempt, return False
    if not expression:
        return float('inf')

    # Get value of expression, or float('inf') if error with expression syntax
    value = evaluate_expression(expression)
    if value == float('inf'):
        return float('inf')

    # If expression evaluates to target, it's a krypto!
    if value == target:
        print("Krypto!")
        return 0

    # If expression evaluates to target + or - 1, it's one off!
    elif value == target + 1:
        print("One off!")
        return 1
    elif value == target - 1:
        print("One off!")
        return -1

    # Otherwise it's not a valid solution
    else:
        print("Evaluates to {}, not {}.".format(value, target))
        return float('inf')


def get_list_expression(attempt, numbers):
    """
        Converts string mathematical expression into a list of all elements
        of given expression.

        Returns False if attempt uses any numbers that aren't in numbers
        list or if attempt uses operations that aren't in ACCEPTED_OPERATORS
        list.

        Parameter: (str) attempt: Mathematical expression with integers,
            +, -, *, /, !, ^, v, (, ), or spaces.
        Parameter: (int) target: Integer that attempt should evaluate to.

        Return: (list): list of strings representing
                numbers and operations from input string. Returns empty list
                if a number in attempt is not in parameter numbers, if any
                characters aren't numbers or in list of approved symbols,
                or if there's the wrong number of operations.
    """

    # Count numbers used
    nums = 0

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
                    return []

                else:
                    # Add to expression list
                    expression.append(current_num_string)
                    current_num_string = ""
                    nums += 1

            # Add valid operations to expression list
            if character in ACCEPTED_OPERATORS:
                expression.append(character)

            # Not operations, but valid symbols to include
            elif character in ["(", ")"]:
                expression.append(character)
            elif character == " ":
                continue

            # Anything else is an invalid symbols
            else:
                print("'" + character + "' is an invalid symbol.", end=' ')
                return []

    # Need to append last number to list
    # Confirm current number is one of the given numbers
    if current_num_string:
        if int(current_num_string) not in numbers:
            print(current_num_string,
                  "isn't one of the given numbers.", end=' ')
            return []
        else:
            # Add to expression list
            expression.append(current_num_string)
            nums += 1

    # Confirm correct number of numbers used
    if nums != 5:
        print("Incorrect number of numbers.", end=' ')
        return []

    # Confirm all numbers used.
    missing_nums = False
    for n in numbers:
        if str(n) not in expression:
            print("Missing number {}.".format(n), end=' ')
            missing_nums = True
    if missing_nums:
        return []

    return expression


def evaluate_expression(expression):
    """
        Evaluate mathematical expression, represented by expression string.

        Parameter: (list) expression: mathematical expression. Each element
                    is a string: integer, arithmetic operation or parentheses.

        Return: (int) value or (bool): value of expression or False if missing
         a close-parentheses.
    """

    # Running value of expression
    value = 0

    # The next operand and operation to perform
    next_operand = 0
    next_operator = ""

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
        elif expression[i] in ACCEPTED_OPERATORS:
            next_operator = expression[i]

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
                    # Can't handle exceptions yet, so return inf
                    return float('inf')

            # Recursively evaluate expression inside parentheses
            if not value:
                value = evaluate_expression(expression[(i + 1):j])
            else:
                next_operand = evaluate_expression(expression[(i + 1):j])

            # skip to other side of parentheses after evaluating val inside
            i = j

        # Evaluate new value based on next_operand and next_operation
        # Factorial is a unary operation.
        if (next_operand and next_operator) or (next_operator == "!"):
            value = operate(value, next_operator, next_operand)

            # Reset next_operand and next_operation so don't enter this block
            # without getting a new next_operand and new next_operation.
            # If operator was factorial, next_operand will already be 0
            next_operand = 0
            next_operator = ""

        # Increment i to iterate through list
        i += 1

    return value


def print_operator_key():
    """
        Prints menu of operations and their corresponding symbols.
    """
    print("*  Multiplication\n"
          "/  Division\n"
          "+  Addition\n"
          "-  Subtraction\n"
          "!  Factorial\n"
          "^  Exponentiation\n"
          "v  Root -- NOTE: Put the index AFTER the √ symbol,\n"
          "           Example: for the cube root of 8, write '8 v 3'\n")


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

    # If max_num is 25, then seeding 14 returns 14, but other seeds can
    # return 14, too.
    if max_num == 25 and seed == 3:
        seed = 2

    # Multiply seed by prime so generated numbers will work their way through
    # all ints between 1 and max_num
    # Add 1 after mod to shift range from [0 to (max_num - 1)]
    # to [1 to max_num]
    num = ((17 * seed + 1) % max_num) + 1

    # Make sure num doesn't = seed
    if num == seed:
        num = (num + 19) % max_num
        if num == seed or num == 0:
            num += 1

    return num


def operate(operand_1, operator, operand_2):
    """
        Performs given mathematical operation on given operands.

        Parameters:
            (int or float) operand_1: first operand
            (string) operation: operation to perform
            (int or float) operand_2: second operand

        Return: (int or float): result of performing operation
    """

    if operator == "*":
        return operand_1 * operand_2

    if operator == "/":
        return operand_1 / operand_2

    if operator == "+":
        return operand_1 + operand_2

    if operator == "-":
        return operand_1 - operand_2

    if operator == "!":
        return factorial(operand_1)

    if operator == "^":
        return operand_1 ** operand_2

    if operator == "v":
        return operand_1 ** (1 / operand_2)


def factorial(num):
    """
        Returns factorial of given number.
        Returns 0 if num is negative or not an integer.
    """
    # Can't take factorial of negatives or non-integers.
    # Running factorial() on a non-integer will eventually hit a negative val.
    if num < 0:
        print("Error: Can only take factorial of positive integers.")
        # Error return 0 because outside expected range and evaluates to False
        return 0

    # Base case
    if num == 0:
        return 1

    # Recursive call
    else:
        return num * factorial(num - 1)


if __name__ == "__main__":
    main()
