""" Modue for Utilities """

from functools import wraps
from time import time


def timer(fn):
    """ Decorator for tracking time """
    @wraps(fn)
    def inner(*args, **kwargs):
        start = time()
        result = fn(*args, **kwargs)
        end = time()
        elapsed = end-start
        print('The program took {0:.2f} seconds.'.format(elapsed))
    return inner


def gen_clean_data(file):
    """ Function to read and clean data

        Args:
        file (str): Path to file

        Returns:
        Generator object

    """
    with open(file) as f:
        for row in f:
            yield row.strip('\n').split(",")
