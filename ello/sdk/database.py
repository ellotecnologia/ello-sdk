import os
import os.path
import subprocess
import glob
import re

EDITOR = os.environ.setdefault("EDITOR", "notepad.exe")
PATCHES_PATH = "database\\patches"


def create_new_sql_patch(args):
    next_patch = get_next_patch_filename()
    notepad = subprocess.Popen([EDITOR, os.path.join(PATCHES_PATH, next_patch)])

    
def get_next_patch_filename():
    """ Gera o nome de um novo patch no formato 'patch_NNN.sql'
    """
    last_patch = sorted(glob.glob(os.path.join(PATCHES_PATH, "patch_*.sql")))[-1]
    patch_number = int(re.search("patch_([0-9]{3})\.sql", last_patch).group(1))
    next_number = patch_number + 1
    return "patch_{:03}.sql".format(next_number)