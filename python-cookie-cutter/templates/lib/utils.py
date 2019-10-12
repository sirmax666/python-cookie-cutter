from datetime import datetime


def example():
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/
    
    SEE: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    """
    pass


def now(fmt='%Y-%m-%d %H:%M:%S'):
    """Function that gives the current timestamp

    Current timestamp given by the operating system.

    Args:
        fmt (str): The timestamp format you which to output the timestamp.

    Returns:
        str: The current timestamp
    """
    return datetime.now().strftime(fmt)
