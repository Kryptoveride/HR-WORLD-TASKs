import re

while True:
    user_input = input("calc> ").strip()

    if user_input.lower() == "exit":
        break

    try:
        if not user_input:
            raise ValueError("Input cannot be empty.")

        if len(user_input) > 50:
            raise ValueError("Input is too long.")

        if not re.fullmatch(r"[0-9+\-*/().\s]+", user_input):
            raise ValueError("Only numbers and basic arithmetic operators are allowed.")

        cleaned_input = re.sub(r"\s+", "", user_input)

        if ".." in cleaned_input:
            raise ValueError("Invalid decimal number.")

        result = eval(cleaned_input, {"__builtins__": {}}, {})
        print(result)

    except ValueError as error:
        print(f"Error: {error}")

    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")

    except SyntaxError:
        print("Error: Invalid mathematical expression.")

    except OverflowError:
        print("Error: The result is too large.")

    except Exception:
        print("Error: Unable to complete the calculation.")