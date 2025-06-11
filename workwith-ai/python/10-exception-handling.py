# Example 1: Basic try-except
try:
    x = 10 / 0  # Attempting division by zero
except ZeroDivisionError:
    print("Error: Division by zero!")

# Example 2: Multiple except blocks
try:
    num = int("abc")  # Attempting to convert string to integer
except ValueError:
    print("Error: Invalid number conversion")
except TypeError:
    print("Error: Type mismatch")

# Example 3: try-except-else-finally
try:
    file = open("example.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("Error: File not found")
else:
    print("File read successfully")
    print(content)
finally:
    file.close() if 'file' in locals() else None

# Example 4: Raising custom exceptions
class CustomError(Exception):
    pass

def check_age(age):
    if age < 0:
        raise CustomError("Age cannot be negative")
    return age

try:
    check_age(-5)
except CustomError as e:
    print(f"Error: {e}")

# Example 5: Using assert
def divide(a, b):
    assert b != 0, "Divisor cannot be zero"
    return a / b

try:
    result = divide(10, 0)
except AssertionError as e:
    print(f"Assertion Error: {e}")
