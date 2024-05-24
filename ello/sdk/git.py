import os
import subprocess
import logging
import shutil
import shlex

logger = logging.getLogger()

FNULL = open(os.devnull, 'w')

def git(args):
    cmd = 'git {0}'.format(args)
    exit_code = subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    return exit_code


def get_last_tag():
    """ Returns the last defined tag in the current repository """
    p = subprocess.Popen(['git', 'describe', '--abbrev=0', '--tags'], stdout=subprocess.PIPE)
    last_tag = p.communicate()[0].strip()
    return last_tag.decode('latin1')


def get_latest_tag():
    """ Get last defined tag from git log
    """
    cmd = 'git rev-list --tags --max-count=1'
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    last_hash = p.communicate()[0].strip()

    cmd = 'git describe --tags {}'.format(last_hash.decode('latin1'))
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].strip().decode('latin1')


def get_sorted_tags():
    """ Returns a list of tags, reachable from the current branch, sorted by date (oldest first) """
    cmd = "git tag --sort=committerdate --merged"
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    lines = p.communicate()[0].decode('latin1')
    tags = lines.splitlines()
    return tags


def get_changes_from(from_tag, from_path):
    """ Retorna uma lista com as mensagens no formato:
        ['- msg <author>', '- msg <author>', ...]
    """
    cmd = ['git', 'log', '--reverse', '--first-parent', '--no-merges', '--pretty=format:%B-> author: <%an>', '{}..'.format(from_tag), from_path]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    git_output = p.communicate()[0].splitlines()
    git_output = map(lambda text: text.decode('utf8'), git_output)
    
    # Coleta apenas a primeira linha da mensagem, ignorando as linhas adicionais.
    changes = []
    try:
        while True:
            message = next(git_output)
            author = ''
            while author == '':
                tmp_line = next(git_output)
                if tmp_line.startswith('-> author: '):
                    author = ' '.join(tmp_line.split()[2:])
            changes.append('- {} {}'.format(message, author))
    except StopIteration:
        pass
    
    return changes


def install_hooks(args):
    """ Instala alguns hooks no repositorio atual """
    if not os.path.exists(".git"):
        print("Repositório git não encontrado")
        return
    hooks_path = os.path.abspath(os.path.dirname(__file__) + "/../../git_hooks")
    for root, dirs, files in os.walk(hooks_path):
        for filename in files:
            shutil.copyfile(os.path.join(hooks_path, filename), ".git/hooks/" + filename)


def repo_has_pending_changes():
    """ Retorna 'True' caso o repositório atual possua modificações não commitadas """
    return_code = subprocess.call("git diff-index --quiet HEAD --", stdout=FNULL, stderr=subprocess.STDOUT)
    return return_code != 0


if __name__ == "__main__":
    if repo_has_pending_changes():
        print('Repositório possui modificações não commitadas')
    else:
        print('Repositório sem nenhuma modificação')
