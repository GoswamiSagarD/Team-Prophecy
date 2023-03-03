import os

def filepath(*args):
    """
    Join multiple strings into a path

    Args:
        *args (str): The strings to join into a path
    Returns:
        str: The path
    """
    return os.path.sep.join(args)