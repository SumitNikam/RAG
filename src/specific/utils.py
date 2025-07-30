import ast
import contextlib
from io import StringIO
import sys


# Function to store python output in an object
@contextlib.contextmanager
def stdoutIO(
    stdout=None
):
    """
    Context manager to capture standard output 
    and return it as a string.

    Args:
        stdout (object, optional): A file-like object to write 
        the output to. If None, a StringIO object is used. 
        Defaults to None.

    Yields:
        object: The stdout object.
    """
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# Function to check if the code is valid python code
def is_valid_python(
    code_string
):
    """
    Checks if the given code string is valid Python code 
    by attempting to parse it with ast.parse().

    Args:
        code_string (str): The code string to check.

    Returns:
        bool: True if the code string is valid Python code, 
        False otherwise.
    """
    try:
        ast.parse(code_string)
        return True
    except SyntaxError:
        return False
