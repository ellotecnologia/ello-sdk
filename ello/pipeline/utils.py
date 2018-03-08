import os
import contextlib
import functools
import glob

def memoize(obj):
    """ Decorator que implementa um memoize
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer

@contextlib.contextmanager
def temp_chdir(path):
    """
    Usage:
    >>> with temp_chdir(gitrepo_path):
    ...   subprocess.call('git status')
    """
    path = path or '.'
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)

def clean_working_dir():
    os.system('del /s *.ddp')
    os.system('del /s *.dsk')
    os.system('del /s *.dcu')
    os.system('del /s *.~*')

def remove_dcus():
    map(os.remove, glob.glob("dcu/*.dcu"))

